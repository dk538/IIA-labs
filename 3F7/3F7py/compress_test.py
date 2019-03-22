from os import stat
from camzip import camzip, camzip_cont
from camunzip import camunzip, camunzip_cont


def run_test(method, filename, context_length):

    if method == 'model':
        camzip_cont(filename)
        filename_zipped = filename + '.cz' + method[0]
        camunzip_cont(filename_zipped)
    if method == 'context':
        camzip(method, filename, cont_length=context_length)
        filename_zipped = filename + '.cz' + method[0]
        camunzip(filename_zipped, cont_length=context_length)
    else:
        camzip(method, filename)
        filename_zipped = filename + '.cz' + method[0]
        camunzip(filename_zipped)

    unzipped = open(filename + '.cuz')
    print(unzipped.read()[:50])

    Nin = stat(filename).st_size
    print(f'Length of original file: {Nin} bytes')
    Nout = stat(filename + '.cz' + method[0]).st_size

    print(f'Length of compressed file: {Nout} bytes')
    print(f'Compression rate: {8.0*Nout/Nin} bits/byte')

    if open(filename).read() == open(filename+'.cuz').read():
        print('The two files are the same')
    else:
        print('The files are different')

    return


if __name__ == '__main__':
    run_test('model', 'hamlet.txt', 3)