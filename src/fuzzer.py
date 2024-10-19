from services.Harness import Harness

def main():
    harness = Harness()
    harness.run_binary('./executables/meme')
    harness.write_hax()

if __name__ == '__main__':
    main()
