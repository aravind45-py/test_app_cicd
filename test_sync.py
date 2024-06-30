from time import perf_counter
import requests



def main():
    start = perf_counter()
    for _ in range(10):
        data = requests.get('https://dog.ceo/api/breeds/image/random')
        print(data)
    print("Seconds Took: ",perf_counter() - start)

if __name__ == '__main__':
    main()