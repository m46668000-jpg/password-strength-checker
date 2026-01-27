import argparse
from password_core import load_common_passwords, analyze_password, hash_password

load_common_passwords()

def main():
    parser = argparse.ArgumentParser(description="Password Strength Checker CLI")
    parser.add_argument("password", help="Password to check")
    parser.add_argument("--hash", action="store_true", help="Show bcrypt hash")
    args = parser.parse_args()

    score, charset, feedback, is_common, entropy, crack_times, zxcvbn_feedback, breached_count = analyze_password(args.password)

    print(f"Password: {args.password}")
    print(f"Score: {score}")
    print(f"Entropy: {entropy:.2f} bits")
    print(f"Common: {is_common}")
    print(f"Breached: {breached_count if breached_count >= 0 else 'Check failed'}")
    print(f"Crack Time (online): {crack_times['online_throttling_100_per_hour']}")
    print(f"Crack Time (offline fast): {crack_times['offline_fast_hashing_1e10_per_second']}")
    if feedback:
        print("Suggestions:")
        for s in feedback:
            print(f"- {s}")
    if zxcvbn_feedback:
        print("Advanced Suggestions:")
        for s in zxcvbn_feedback:
            print(f"- {s}")
    if args.hash:
        print(f"Bcrypt Hash: {hash_password(args.password)}")

if __name__ == "__main__":
    main()