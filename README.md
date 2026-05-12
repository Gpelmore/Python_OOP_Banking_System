A command-line banking interface built entirely in standard Python to demonstrate Object-Oriented Programming (OOP) principles, secure 
data handling, and stateful application architecture.

The system operates through a modular backend separating financial logic from user authentication. Users can register accounts, login 
securely via SHA-256 hashed and salted passwords, and perform core banking transactions (Withdraw, Deposit, Transfer) across multiple 
account types. The application heavily emphasizes security and user state, featuring unique cryptographic session tokens, a dynamic 
rolling idle timeout, and rate-limiting to temporarily freeze accounts subjected to brute-force login attempts.
