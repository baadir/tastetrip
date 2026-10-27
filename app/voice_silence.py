"""Bounded silence policy plus a small mu-law activity detector."""


def has_voice(audio):
    if not audio: return False
    energy = 0
    for byte in audio:
        value = (~byte) & 255
        sample = ((((value & 15) << 3) + 132) << ((value >> 4) & 7)) - 132
        energy += sample * sample
    return energy / len(audio) >= 600 * 600


class SilenceGuard:
    def __init__(self, now):
        self.last = now
        self.prompted = False
    def heard(self, now):
        self.last = now
        self.prompted = False
    def tick(self, now, assistant_speaking=False):
        if assistant_speaking:
            self.heard(now)
            return None
        elapsed = now - self.last
        if elapsed >= 10: return "hangup"
        if elapsed >= 4 and not self.prompted:
            self.prompted = True
            return "check"
        return None
