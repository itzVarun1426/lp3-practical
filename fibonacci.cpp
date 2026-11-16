#include <iostream>
using namespace std;

// Non-recursive (Iterative) function
int fibonacciNonRecursive(int n) {
    int a = 0, b = 1, c;

    if (n == 0)
        return a;

    for (int i = 2; i <= n; i++) {
        c = a + b;
        a = b;
        b = c;
    }

    return b;
}

// Recursive function
int fibonacciRecursive(int n) {
    if (n == 0)
        return 0;

    if (n == 1)
        return 1;

    return fibonacciRecursive(n - 1) + fibonacciRecursive(n - 2);
}

int main() {
    int n;

    cout << "Enter the position: ";
    cin >> n;

    if (n < 0) {
        cout << "Please enter a non-negative number.";
        return 0;
    }

    cout << "Non-Recursive Fibonacci: ";

    for (int i = 0; i < n; i++) {
        cout << fibonacciNonRecursive(i) << " ";
    }

    cout << "\nRecursive Fibonacci: ";

    for (int i = 0; i < n; i++) {
        cout << fibonacciRecursive(i) << " ";
    }
}
