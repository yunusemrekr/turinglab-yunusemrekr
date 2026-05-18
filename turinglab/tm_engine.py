import yaml
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Configuration:
    state: str
    tape: str
    head_position: int

@dataclass
class RunResult:
    accepted: bool
    final_tape: str
    steps: int
    history: List[Configuration]
    reason: str = ""

class Tape:
    """Tek şeritli bant temsilcisi"""
    def __init__(self, input_string: str, blank_symbol: str = "B"):
        if not input_string:
            self.content = [blank_symbol]
        else:
            self.content = list(input_string)
        self.blank = blank_symbol
        self.head = 0

    def read(self) -> str:
        return self.content[self.head]

    def write(self, char: str):
        self.content[self.head] = char

    def move(self, direction: str):
        if direction == 'R':
            self.head += 1
            if self.head >= len(self.content):
                self.content.append(self.blank)
        elif direction == 'L':
            self.head -= 1
            if self.head < 0:
                self.content.insert(0, self.blank)
                self.head = 0
                
    def get_tape_string(self) -> str:
        return "".join(self.content)

    def get_verbose_tape(self) -> str:
        # Kafa pozisyonunu köşeli parantez içinde gösteren format
        left = "".join(self.content[:self.head])
        head_char = f"[{self.content[self.head]}]"
        right = "".join(self.content[self.head+1:])
        return left + head_char + right

class SingleTapeTM:
    """Deterministik Tek Şeritli Turing Makinesi"""
    def __init__(self, tm_def: Dict[str, Any]):
        self.name = tm_def.get("name", "Unknown")
        self.states = tm_def.get("states", [])
        self.input_alphabet = tm_def.get("input_alphabet", [])
        self.tape_alphabet = tm_def.get("tape_alphabet", [])
        self.blank = tm_def.get("blank", "B")
        self.start_state = tm_def.get("start_state", "")
        self.accept_states = tm_def.get("accept_states", [])
        self.reject_states = tm_def.get("reject_states", [])
        
        self.transitions = {}
        for t in tm_def.get("transitions", []):
            self.transitions[(t["state"], t["read"])] = (t["next"], t["write"], t["move"])

    @classmethod
    def from_yaml(cls, filepath: str) -> "SingleTapeTM":
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                tm_def = yaml.safe_load(f)
            if not isinstance(tm_def, dict) or "states" not in tm_def or "transitions" not in tm_def:
                raise ValueError(f"Hatalı YAML formatı veya eksik alanlar: {filepath}")
            return cls(tm_def)
        except Exception as e:
            raise ValueError(f"YAML yüklenirken hata oluştu: {e}")

    def run(self, input_string: str, max_steps: int = 1000, verbose: bool = False) -> RunResult:
        tape = Tape(input_string, self.blank)
        current_state = self.start_state
        steps = 0
        history = []
        
        history.append(Configuration(state=current_state, tape=tape.get_tape_string(), head_position=tape.head))

        while steps < max_steps:
            if current_state in self.accept_states:
                return RunResult(accepted=True, final_tape=tape.get_tape_string(), steps=steps, history=history, reason="accept")
            if current_state in self.reject_states:
                return RunResult(accepted=False, final_tape=tape.get_tape_string(), steps=steps, history=history, reason="reject")

            current_symbol = tape.read()
            transition_key = (current_state, current_symbol)
            
            if transition_key in self.transitions:
                next_state, write_sym, move_dir = self.transitions[transition_key]
                
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şerit: {tape.get_verbose_tape()} | Hareket: {move_dir}")
                    
                tape.write(write_sym)
                tape.move(move_dir)
                current_state = next_state
                steps += 1
                
                history.append(Configuration(state=current_state, tape=tape.get_tape_string(), head_position=tape.head))
            else:
                if verbose:
                    print(f"Adım {steps} | Durum: {current_state} | Şerit: {tape.get_verbose_tape()} | Hareket: Yok (Çöktü)")
                return RunResult(accepted=False, final_tape=tape.get_tape_string(), steps=steps, history=history, reason="no_transition")

        return RunResult(accepted=False, final_tape=tape.get_tape_string(), steps=steps, history=history, reason="timeout")
