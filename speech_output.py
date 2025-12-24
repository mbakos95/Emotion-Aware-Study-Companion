# speech_output.py
import subprocess

class SpeechOutput:
    def __init__(self, rate=0, volume=100, voice_name=None):
        # rate: -10..10 (SAPI style), volume: 0..100
        self.rate = int(rate)
        self.volume = int(volume)
        self.voice_name = voice_name  # optional partial name match

        # PowerShell script reads text from stdin and speaks it
        self.ps_script = r"""
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.Rate = {RATE}
$synth.Volume = {VOLUME}
{VOICE_SELECT}
$text = [Console]::In.ReadToEnd()
if ($text -and $text.Trim().Length -gt 0) {{ $synth.Speak($text) }}
""".strip()

    def speak(self, text: str):
        if not text or not text.strip():
            return

        voice_select = ""
        if self.voice_name:
            # try to select voice by partial match
            voice_select = f"""
$voice = $synth.GetInstalledVoices() | ForEach-Object {{ $_.VoiceInfo.Name }} | Where-Object {{ $_ -like '*{self.voice_name}*' }} | Select-Object -First 1
if ($voice) {{ $synth.SelectVoice($voice) }}
""".strip()

        script = self.ps_script.format(
            RATE=self.rate,
            VOLUME=self.volume,
            VOICE_SELECT=voice_select
        )

        subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
            input=text,
            text=True
        )
