import os
from os import path
import matplotlib.pyplot as plt
import numpy as np

ROOT = r'I:\1_RawData\SingleMoleculeData\smFRETtraces_MolecularSortingCompetition\FRET_corrected\ebsibs_2.5mMMg'

OUTPUT_DIR = r'D:\output'

DEBUG = False
DEBUG_FILE = ROOT + r'\IBS-25mM-Mg_1_all231_mol8_post.txt'


EXTENSIONS = ['.txt']



def generatePlot(filePath):
    print 'generating plot for ' + filePath
    values = []
    lines = 0
    with open(filePath, 'r') as f:
        tempVals = [[],[],[]]
        for line in f:
            if not line.startswith('#'):
                lines += 1
                temp = map(float, line.split())
                tempVals[0].append(temp[0])
                tempVals[1].append(temp[1])
                tempVals[2].append(temp[2])
        for entry in tempVals:
            values.append(np.array(entry))

    if not values:
        print 'no values!!!'
        return ''
    

    title = filePath.split('\\')[-1].split('.')[0]
    x = np.arange(0, lines, 1)

    fig, axs = plt.subplots(2, 1, sharex=True)
    fig.subplots_adjust(hspace=0)
    axs[0].set_title(title)
    
    axs[0].set(ylabel='Intensity')
    axs[1].set(ylabel='FRET', xlabel = 'frame number')

    # axs[0].plot(x, values[0], 'g', x, values[1], 'r', label = 'bla', linewidth=0.5)
    axs[0].plot(x, values[0], color='green', linewidth=0.5)
    axs[0].plot(x, values[1], color='red', linewidth=0.5)
    axs[1].plot(x, values[2], color='black', linewidth = 0.5)

    fig.align_ylabels(axs)

    targetPath = OUTPUT_DIR + '\\' + title + '.png'
    # print targetPath
    plt.savefig(targetPath)
    plt.close(fig)
    # plt.show()

    return ''


if __name__ == "__main__":
    if DEBUG:
        generatePlot(DEBUG_FILE)    
    else:
        countFiles = 0
        results = []

        print('start iterating files')
        for root, dirs, files in os.walk(ROOT):
            for file in files:
                if any(file.endswith(ext) for ext in EXTENSIONS):
                    filePath = path.join(root, file)
                    # print(filePath)
                    resultPath = generatePlot(filePath)
                    results.append(resultPath)

            countFiles += len(files)


        print('countFiles: ' + str(countFiles))
        # print(results)    
