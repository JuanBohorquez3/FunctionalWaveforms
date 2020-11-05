# FunctionalWaveforms
Functional Waveforms in the hybrid experiment

To use a file in this repo as your functional waveform, add the following code to you functional waveforms text input box:

    import os

    waveforms_path = "C:\Users\Hybrid\Repos\FunctionalWaveforms"
    file_name = "Base_Waveform.py"

    waveform_file = os.path.join(waveforms_path,file_name)

    text = ""

    try:
        with open(waveform_file,'r') as f:
            for line in f:
                text = text+line
    except IOError as e:
        print("{}\n file = {}".format(e,waveform_file))
        raise

    exec(text)
