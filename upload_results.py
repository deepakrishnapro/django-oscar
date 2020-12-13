#!/usr/bin/env python3

def main():
    try:
        print('Calling a function upload tests ')

    except Exception as exception:
        print("Exception occurred during running upload results  for pipeline-id - Exception details : {}".format(str(exception)))
        pass

if __name__ == "__main__":
    main()
