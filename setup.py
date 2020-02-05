from cx_Freeze import setup, Executable



options = {
    'build.exe': {
    'icludes': [
    'correct.ui', 'CorrectDiary.py', 'dnevnik.ui', 'notebook.ui',
    'settings.ui',
    ]
    }
}
setup(
    name='Diary',
    version='1.0',
    description='a',
    option=options,
    executables=[Executable('Diary.py')]
)