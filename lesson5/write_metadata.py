import nbformat
import sys

def readNotebook(pathToNoteBook):
    with open(pathToNoteBook, 'r') as f:
        nb = nbformat.read(f, as_version=4)
    return nb

def writeMetadataToCodeCells(notebook):
    i_nb = iter(notebook.items())
    cells = next(i_nb)[1]

    for c in cells:
        if c['cell_type'] == 'code':
            # write metadata to the code cell
            c['metadata']['execute'] = True
            print('\n')
            print(c)
            print('\n')

def updateNotebook(notebookObj, pathToNoteBook):
    with open(pathToNoteBook, 'w') as f:
        nbformat.write(notebookObj, f, version=4)


if len(sys.argv) != 2:
    print("Invalid number of arguments")
    sys.exit(-1)

notebookFilePath = sys.argv[1]

nb = readNotebook(notebookFilePath)
writeMetadataToCodeCells(nb)
updateNotebook(nb, notebookFilePath)