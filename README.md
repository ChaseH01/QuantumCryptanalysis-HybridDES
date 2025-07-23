# QuantumCryptanalysis-HybridDES
I built a small scale DES (only one iteration instead of 16) and then built a quantum simulation to crack the encryption using Grover's Algorithm:

Full Report:
Algorithm Recap: Summary of HBEA structure. 
High-level summary:
	We accept an email to generate a random key.
	Store or retrieve a custom IP table and its inverse unique to each email.
	Encrypt 32-bit blocks by applying a Feistel structure, emulating DES encryption.
	Decrypt by applying the same operations in order, using the ciphertext to retrieve the plaintext.
Key Generation:
	We hash a user provided email to generate a random key of 32 bytes (256 bits) 
	We apply the user’s unique initial permutation to the key and then store the key as two halves, each with 16 bytes.
Message Processing:
	We take the plaintext message of 32 bytes and apply the user’s unique initial permutation on the message. We store this processed message in two halves, each with 16 bytes.
Encryption Process:
	We take the right half of the permuted plaintext and expand it using the standard DES expansion table. We do this one 32-bit block at a time, so we expand each 32 bits (4 bytes) into 48 bits.
	We expand the corresponding key block to the expanded message block.
	We XOR the expanded key block and its corresponding expanded message block.
	We pass the result through the standard DES S-boxes to go from 48 bits, back to 32 bits.
	Lastly, we XOR the S-box output with the saved left half of the message that remained untouched during this process.
	We repeat this process for each block of plaintext, concatenating the results until we are left with our ciphertext.
Decryption Process:
	 We expand a 32-bit block of ciphertext into 48 bits using our expansion table.
	We expand the corresponding key block using the same expansion table.
	XOR the expanded key block and its corresponding expanded ciphertext block.
	Pass the result through the s-boxes to go return to 32 bit blocks.
	Finally, XOR the s-box output with the original, untouched left half of the message block.
	Repeat this process for each block of ciphertext, concatenating the results.
	We apply the inverse permutation table, resulting in the original plaintext.
Benchmark Table: HBEA vs AES-256. 
Creator	Me (Chase Hurwitz) HBEA	U.S. National Institute of Standards and Technology (NIST) AES
Cryptographic Logic	Based on DES (Data Encryption Standard), but customized with dynamic permutations and key generation	AES (Advanced Encryption Standard), specifically Rijndael algorithm
Block Size	32 bits (inherited from DES)	128 bits
Key Size	256 bits, derived from SHA-256(email) and broken into 8 one-byte segments	256 bits (32 bytes), used as a whole
Rounds	Only one – only has the capacity to perform a single round of encryption on 256 bits (DES uses 16 rounds)	14 rounds for AES-256
Key Schedule	Fixed permutation of hash-based segments and runtime-shuffled tables, although shuffling is done predictably.	Complex key expansion algorithm with round keys
Permutation Tables	Randomized per user (via JSON persistence); includes IP and IP⁻¹	Fixed S-boxes and permutation structure
Substitution	Uses 8 standard DES S-boxes	Uses a single 16×16 Rijndael S-box
Expansion	DES-style expansion to 48 bits for S-box input	No expansion (AES uses byte substitution + matrix operations)
Cryptographic Strength	Untested – 256-bit key is strong, but using emails to generate them is weak and predictable.	Industry standard — widely tested and secure against known practical attacks
Performance	Slower due to JSON I/O, SHA-256 + dynamic key generation	Highly optimized in hardware and software
Security Concerns	- If an attacker has access to a user’s email, they can derive their key and access their IP IP-1
- S-box reuse (from DES) is a known weakness
- User-specific randomness must be cryptographically secure	Secure against brute force, side-channel attacks, and chosen plaintext attacks when implemented properly
Flexibility	User-adaptive key system allows per-user customization of permutation tables	Standardized and uniform for all users
Use Case 	Educational or niche personal encryption; experimental	Government, military, enterprise-grade data encryption
Standardization	None (experimental)	Fully standardized (FIPS 197)

Quantum Simulation: Output or screenshots.
Goal: Simulate a quantum attack using Grover’s Algorithm.
Overview: Grover’s Algorithm is a quantum search algorithm used to search unsorted, unstructured databases in O(√N) time. This is much more efficient than a classic algorithm that would rely on brute force in O(N) time.
Our simulation: Our HBEA utilizes SHA-256 to create a key of 256 bits. In the real world, that would take Grover’s algorithm 2^128 iterations to find the key which is too big even for quantum computers, let alone a classic laptop with Qiskit. So instead, we scale down our key to 4 bits to demonstrate the proper quantum principles. With a 4-bit target, we utilize 4 qubits to represent the solution space which instead of having 2^256possibilities, now only has 2^4 or 16 possibilities which is a much more computationally feasible job for a laptop, while still being conceptually illustrative.
Justification: Grover’s algorithm complexity scales at O(√N) regardless of N. Therefore, we can extrapolate our findings from a small simulation to a full 256-bit key target in order to analyze how Grover’s algorithm would perform on our HBEA.





Methodology: 
	Initialization: we create a quantum circuit with 4 qubits and 4 matching classical bits. 
	Superposition: Hadamard gates are applied to all qubits, placing them in a uniform superposition of all 16 possible solutions.
	Oracle Construction: We marked the target key |1011> by flipping any qubit where the target bit was 0. Then, we apply multi-controlled-Z operations, and then unflip those qubits which inverts the amplitude of the target key.
	Diffusion Operator: We apply another round of Hadamard, X, and multi-controlled-Z gates to reflect the amplitudes over the mean.
	Measurement and Simulation: We added measurement gates to all qubits and simulated the circuit 1024 times (an appropriately large number to see meaningful trends). 
Results:
The measured results show our target key of |1011> occurred 455 out of 1024 times, significantly higher than any other state. All other states stayed consistently low at 27-47 measurements. This outcome demonstrates a successful implementation of Grover’s Algorithm, as it increased the amplification of the correct state, while minimizing the other state’s amplitudes. Therefore, these results demonstrate how Grover’s Algorithm can drastically improve search results in unsorted, unstructured solution spaces.











Visualizations:
Before simulation/measurement
 
Figure 1: Bloch Spheres showing the initial state of the 4 qubits before simulation.
 

Figure 2: A 3D representation of a quantum statevector, illustrating the probability amplitudes prior to measurement, with heightened bars indicating states with larger amplitudes, and thus a higher probability of being measured. 








After simulation/measurement:
 
Figure 3: demonstrates the frequency each possible state was observed after running our circuit 1,024 times.

 
Figure 4: visualizes the measurement data in a histogram, clearly demonstrating Grover’s Algorithm accurately observed our target key significantly more than others.
 
Figure 5: Grover circuit observed after measurement, showing depicting the gates.
Extrapolation:
My HBEA algorithm utilizes a 256-bit key by hashing a user’s email using SHA-256. To represent this solution space, Grover’s Algorithm would require 256 qubits (one per bit) to represent the superposition of all 2^256 solutions. Additionally, we will likely need extra ancillary qubits to help perform intermediary steps like multi-controlled NOTs or phase flips. These qubits do not represent the input/output but are needed to perform complex circuit computations. In our small-sized simulation with four qubits, we did not need any ancillary qubits because the operations remained simple enough, but cracking a 256-bit key could require hundreds or thousands of ancillary qubits.
The number of Grover iterations to identify a key of length N grows at O(√N). Thus, for both my HBEA or AES-256 where N = 256, the worst-case time complexity equals 2^128 operations, each requiring multiple quantum gate operations. Executing 2^128 iterations is practically infeasible even for a quantum computer at this point. Thus, HBEA’s strength is maintained because 2^256 is still a sufficiently large solution space that even a quantum computer would struggle to brute force it. But, in the future, as quantum technology gets better and cheaper, and companies build quantum computers with more and more qubits, brute forcing a solution space of 2^256 could be possible. 
Quantum Resistance:
Grover’s algorithm provides a quadratic speed-up over traditional brute force search. What would take O(N) time, can be completed in O(√N). However, my HBEA generates its random key from SHA-256, meaning N = 256 bits, and thus Grover’s Algorithm’s worst-case complexity for cracking a password is  2^128 operations. This is still sufficiently large enough to withstand brute force attacks from quantum computers. For comparison, AES-128 is still considered quantum resistant according to NIST PQC evaluation criteria. This means that Grover’s Algorithm would need to complete 2^64 operations to find the key which is still infeasible for a quantum computer. Therefore, our HBEA algorithm is quantum resistant to modern quantum attacks for the foreseeable future.
AES-256 VS HBEA:
Metric	AES-256	HBEA
Key size	256 bits	256 bits
Classic brute force operations	 2^256	 2^256
Grover Algorithm operations	 2^128	 2^128
Structure	Block cipher	Hash-based (SHA-256)
Oracle Complexity	Requires reversible AES	Requires reversible SHA-256

Theoretically, Grover’s Algorithm equally weakens both AES-256 and my HBEA by reducing the solution space from  2^256 to  2^128. But in practice, my HBEA may be even more secure than AES-256 due to the oracle complexity. Quantum circuits must be reversible at the gate-level: AES-256 is built with relatively simple operations (XOR, substitutions, etc.) which can be reversible. Thus, to build an AES oracle would be very complex, but possible (in fact, AES Grover Oracles already exist). But, SHA-256 is hash function and is thus intentionally built to be one-way using complex operations like bit-mixing, additions, and non-linear compressions. So, to implement the reversible circuit needed to run Grover’s Algorithm would be incredibly difficult for SHA-256. Therefore, in actuality, building a SHA-256 Grover Oracle would likely be much more difficult (and require many more qubits) than building that for AES-256. Therefore, while Grover’s Algorithm theoretically weakens both AES-256 and my HBEA the same amount, in practice, I believe my HBEA is actually stronger due to the one-way nature of SHA-256.
HBEA NIST Compliance Evaluation
	Key Length: Key lengths of 256 bits are considered secure against classical brute force and quantum attacks per NIST. My HBEA meets this standard with a 256-bit key.
	Permutation Strength: NIST recommends that block ciphers should utilize non-linear operations and diffusion to ensure secure encryption. My HBEA utilizes both of those in a Feistel structure with S-boxes, permutations, and shifting. Thus, my HBEA meets this standard.
	Padding Scheme: NIST recommends unambiguous and securely reversible padding for block alignment. My HBEA does not have a padding scheme and requires exactly 32 characters or a full 256-bit block as plaintext. This represents a potential weakness as attackers always know the length of the plaintext. Thus, this aspect of my HBEA is not NIST compliant.
	Random and Secure Key Generation: We use SHA-256 to generate our keys which is endorsed by NIST. That being said, we are deriving these keys from potentially predictable inputs (like emails) – so if an attacker gains access to a user’s email, then they can almost immediately derive their key, meaning the secure length of 256-bits would be irrelevant. To truly be secure, we could replace SHA-256 with a key derivation function (KDF) and store each salted version in a database, keeping the functionality where each user gets a unique key, but removing the predictable email input.
	Key Storage: keys should be stored securely with hardware protection, or encrypted software key stores, and never in plaintext. My HBEA never stores any keys directly which is good, but it does store the emails used to generate these keys in plaintext in a JSON file. This JSON file then becomes an attack target because access to it essentially gives away all the sensitive information about a user and allows them to immediately derive their key by hashing their email. To meet NIST recommendations, it would be better to utilize a KDF with email + password + user specific salt as inputs.

Vulnerability Analysis: Issues and proposed fixes. 
	Weak key derivation: 
	Issue: Creating a key based on a user’s email alone is not secure. An attacker would only need to guess a user’s email to learn their key which would be far less difficult than brute-force guessing the 256-bit key. Also, it is very likely an attacker could gain access to their email somehow which would also be insecure for our user.
	Solution: replace our SHA-256 key generation with an actual KDF like Argon2id.
	Poor Data Storage:
	Issue: We store the user’s email and their unique IP IP-1 tables in a JSON file. Incredibly sensitive information is stored in plaintext in this file and an attacker would be able to decrypt every secure message if they gained access to this JSON file.
	Solution: We should use more secure storage methods like a relational database with encrypted fields. If not, we could at least encrypt a user’s email and IP, IP-1 tables before inserting them into the JSON file so that an attacker cannot easily gain this information if the JSON gets compromised.
	Non-existent Data Padding:
	 My HBEA does not implement data padding for a user’s plaintext. If they do not provide a plaintext message of exactly 32 bytes, the algorithm will not accept it and instead use a default message of 32 characters. If an attacker knows that the plaintext needs to be exactly 32 characters, they can easily target that exact input length to brute force.
	Solution: We should utilize standard padding schemes like PKCS #7. This would add bytes to fit the necessary block size and thus add randomness to the encryption.
<img width="468" height="623" alt="image" src="https://github.com/user-attachments/assets/856f79f4-cf26-4ccc-a7d4-ab57ed412c2d" />

