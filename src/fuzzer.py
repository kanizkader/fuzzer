import os
from services.Harness import Harness

def main():
    harness = Harness()

    binary_path = './binaries'
    for filename in os.listdir(binary_path):
        path = os.path.join(binary_path, filename)
        harness.run_binary(path)
        harness.write_hax(filename)

if __name__ == '__main__':
    main()
