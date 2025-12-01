"""
Brian2 Driver Module.

Implements the digital twin driver using the Brian2 simulator.
"""

import brian2 as b2
import numpy as np
from typing import List, Any
from .base import ElectrophysiologyDriver
from ..biocompiler.isa import OpCode, Instruction
from ..opu.device import OPU

class Brian2Driver(ElectrophysiologyDriver):
    """
    Driver for the Brian2-based Digital Twin.
    """
    
    def __init__(self, opu: OPU):
        self.opu = opu
        self.network = None
        self.neurons = None
        self.J = None
        self.h = None
        self.sigma = 0.0
        
    def connect(self):
        """Initialize the Brian2 environment."""
        # Reset Brian2 scope
        b2.start_scope()
        # Set default clock
        b2.defaultclock.dt = 0.1 * b2.ms
        
    def disconnect(self):
        """Clean up resources."""
        self.network = None
        self.neurons = None
        
    def execute(self, instructions: List[Instruction]) -> Any:
        """
        Execute BioASM instructions using Brian2.
        """
        results = {}
        
        for instr in instructions:
            if instr.opcode == OpCode.ALC:
                self._allocate(instr.operands[0])
            elif instr.opcode == OpCode.LDJ:
                self.J = np.array(instr.operands[0])
            elif instr.opcode == OpCode.LDH:
                self.h = np.array(instr.operands[0])
            elif instr.opcode == OpCode.SIG:
                self.sigma = float(instr.operands[0])
                # Update noise in the neuron model dynamically
                if self.neurons:
                    # We need to access the variable in the running network
                    # Brian2 allows setting variables directly
                    self.neurons.sigma_noise = self.sigma * b2.volt
            elif instr.opcode == OpCode.RUN:
                duration = float(instr.operands[0])
                self._run_simulation(duration)
            elif instr.opcode == OpCode.RD:
                # Read state (final membrane potentials)
                if self.neurons:
                    results['state'] = np.array(self.neurons.v[:])
                
        return results
        
    def _allocate(self, num_neurons: int):
        """Create the neuron group with Critical Regime parameters."""
        # Hardcoded Critical Regime Parameters as requested
        R = 50 * b2.Mohm
        tau = 20 * b2.ms
        El = -70 * b2.mV
        Vt = -50 * b2.mV
        Vr = -70 * b2.mV
        I_offset = 0.36 * b2.nA
        # Initial sigma (will be updated by SIG instruction)
        sigma_init = 2.0 * b2.mV 
        
        # Brian2 equations
        # dv/dt = (-(v - El) + R * (I_offset + I_input)) / tau + sigma_noise * sqrt(2/tau) * xi : volt
        eqs = '''
        dv/dt = (-(v - El) + R * (I_offset + I_input)) / tau + sigma_noise * sqrt(2/tau) * xi : volt
        I_input : amp
        sigma_noise : volt
        '''
        
        self.neurons = b2.NeuronGroup(
            num_neurons,
            eqs,
            threshold='v > Vt',
            reset='v = Vr',
            method='euler'
        )
        
        # Initialize variables
        self.neurons.v = El # Start at rest
        self.neurons.sigma_noise = sigma_init
        self.neurons.I_input = 0 * b2.amp
        
        # Create Network
        self.network = b2.Network(self.neurons)
        
        # Add feedback loop
        @b2.network_operation(dt=1*b2.ms)
        def feedback_loop():
            if self.J is not None and self.h is not None:
                # 1. Get State 's'
                # We use a normalized potential approximation for the state
                # s \in [0, 1]
                v_raw = self.neurons.v / b2.volt
                el_raw = El / b2.volt
                vt_raw = Vt / b2.volt
                
                # Linear mapping of v to [0, 1]
                s = np.clip((v_raw - el_raw) / (vt_raw - el_raw), 0, 1)
                
                # 2. Compute Feedback Current
                # I_fb = J @ s + h
                # We assume J and h are dimensionless or scaled to produce Amperes
                # But to ensure stability, we normalize the output current
                
                raw_current = (self.J @ s + self.h)
                
                # 3. Normalize Feedback
                # Target range: +/- 1.5 nA
                target_range = 1.5e-9
                
                # We apply a scaling factor if the current is too large
                # Or we just clip it?
                # The prompt says: "Implement automatic normalization so feedback J*s doesn't saturate neurons"
                # "Keep injection current in range +/- 1.5 nA"
                
                # Let's clip it to be safe, assuming J was already somewhat normalized
                # But better to scale it if it exceeds the range to preserve relative structure
                max_abs_current = np.max(np.abs(raw_current))
                if max_abs_current > target_range:
                    scale = target_range / max_abs_current
                    raw_current = raw_current * scale
                
                self.neurons.I_input = raw_current * b2.amp
                
        self.network.add(feedback_loop)
        
    def _run_simulation(self, duration: float):
        """Run the simulation."""
        if self.network:
            self.network.run(duration * b2.second)
