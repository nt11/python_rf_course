import time



if __name__ == "__main__":
    print("Results")
    print("-------")
    t1 = time.perf_counter()
    time.sleep(1.2)
    t2 = time.perf_counter()

    print(f"Time slept: {t2-t1}")