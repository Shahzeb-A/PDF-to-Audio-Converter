import PyPDF2 as pypdf
from gtts import gTTS
from appJar import gui
from pathlib import Path
import os


def pdf_to_audio(input_directory, output_directory):
    for file in os.listdir(input_directory):
        directory = f'{input_directory}/{file}'
        pdfFileObj = open(directory, 'rb')
        pdfReader = pypdf.PdfFileReader(pdfFileObj)

        myText = ''

        for pageNum in range(pdfReader.numPages):
            pageObj = pdfReader.getPage(pageNum)

            myText += pageObj.extractText()
        pdfFileObj.close()

        tts = gTTS(text=myText, lang='en')
        save = f'{output_directory}/{file}.mp3'
        tts.save(save)

    print(f'File Saved')


def validate_inputs(src_dir, destination_dir):
    errors = False
    error_msgs = []

    accepted_files = []
    for file in os.listdir(src_dir):
        if file.endswith('.pdf'):
            accepted_files.append(file)
    if len(accepted_files) < 1:
        errors = True
        error_msgs.append('Please select a correct directory with a PDF file')

    if not Path(destination_dir).exists():
        errors = True
        error_msgs.append('Please Select a correct output directory')

    return errors, error_msgs


def press(button):
    if button == 'Process':
        src_file = app.getEntry('Input_Directory')
        destination_dir = app.getEntry('Output_Directory')
        errors, error_msg = validate_inputs(src_file, destination_dir)
        if errors:
            app.errorBox('Error', '\n'.join(error_msg), parent=None)
        else:
            pdf_to_audio(src_file, Path(destination_dir, destination_dir))
    else:
        app.stop()


# Add the Interactive Components
app = gui('PDF To Audio Converter', useTtk=True)
app.setTtkTheme('alt')
app.setSize(500, 200)

app.addLabel('Choose a PDF File to Convert it to an Audio file')
app.addDirectoryEntry('Input_Directory')

app.addLabel('Select Output Directory')
app.addDirectoryEntry('Output_Directory')

app.addButtons(['Process', 'Quit'], press)
app.go()
