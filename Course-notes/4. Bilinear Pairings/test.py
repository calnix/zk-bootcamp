import threading
from py_ecc.bn128 import G1, G2, pairing, add, multiply, eq

def perform_ecc_operations():
    try:
        A = multiply(G2, 32)
        B = multiply(G1, 6)
        C = pairing(A, B)
        print("ECC operations completed successfully")
        print(C)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

def main():
    # Set a timeout value in seconds (e.g., 10 seconds)
    timeout = 300

    # Create a thread for ECC operations
    ecc_thread = threading.Thread(target=perform_ecc_operations)

    # Start the ECC thread
    ecc_thread.start()

    # Wait for the ECC thread to finish or timeout
    ecc_thread.join(timeout)

    # If the thread is still running (timed out), stop it
    if ecc_thread.is_alive():
        print("ECC operations timed out")
        ecc_thread.join()  # Ensure the thread is terminated

if __name__ == "__main__":
    main()
