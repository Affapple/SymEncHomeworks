#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "./enigma.c"
#include "./utils.c"

void N(char* key, char* msg, int* out, int cribLength) {
    // message key (rotors state)
    int n_shift = to_int(key[0]);
    int m_shift = to_int(key[1]);

    int i = 0;
    while (msg[i] && i < cribLength) {
        int c = to_int(msg[i]);

        int p2 = 0;
        if (n_shift == notch[0] || m_shift == notch[1]) p2 = 1;
        
        n_shift = (n_shift + 1) % 26;
        if (p2) m_shift = (m_shift + 1) % 26;

        /* ROTOR1 */
        c = (c + n_shift) % 26;
        c = rotor[0][c];
        c = (c - n_shift + 26) % 26;

        /* ROTOR2 */
        c = (c + m_shift) % 26;
        c = rotor[1][c];
        c = (c - m_shift + 26) % 26;

        out[i] = c;
        i++;
    }
}

void baton_method(char* known_ciphertext, char* crib) {
    char key[3] = {0}; // Date Key
    int cribLength = strlen(crib);
    int N_c[cribLength];
    int N_p[cribLength];

    // array of alphabetic keys
    int potentialKeys[26] = {0}; 
    int keyIdx = 0; // Index for potentialKeys

    // We cannot assume 2nd rotor does not turn,
    // according to guidelines
    for (char rotor2_pos = 'A'; rotor2_pos <= 'Z'; rotor2_pos++) {
        key[1] = rotor2_pos;
        for (char rotor1_pos = 'A'; rotor1_pos <= 'Z'; rotor1_pos++) {
            key[0] = rotor1_pos;
            N(key, crib, N_p, cribLength);
            N(key, known_ciphertext, N_c, cribLength);

            // Verify encryptions for inconsistencies
            int isContradictory = 0; // assume its not contradiction
            int mapping[26] = {[0 ... 25] = -1}; // -1 means no mapping, otherwise maps to the value
            for (int i = 0; i < cribLength; i++) {
                int plain_translation = N_p[i];
                int cipher_translation = N_c[i];

                // plain_translation  -> cipher_translation
                // so
                // cipher_translation -> plain_translation 
                if (mapping[plain_translation] == -1 && mapping[cipher_translation] == -1) {
                    mapping[plain_translation] = cipher_translation;
                    mapping[cipher_translation] = plain_translation;
                    continue;
                }
                if (mapping[plain_translation] != cipher_translation || mapping[cipher_translation] != plain_translation) {
                    isContradictory = 1;
                    break;
                }
            }
            if (!isContradictory) {
                // Save the potential key of the first rotor position
                potentialKeys[to_int(key[0])] = 1; 
                keyIdx++;
            }
        }
    }

    printf("Potential first rotor positions:\n");
    for (int i = 0; i < 26; i++) {
        if (potentialKeys[i] == 1) {
            printf("%c, ", 'A' + i);
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc < 3) {
        printf("Usage: %s <ciphertext_file> <crib>\n", argv[0]);
        return EXIT_FAILURE;
    }
    char* filename = argv[1];
    char* crib = argv[2];
    char* known_ciphertext = getTextFromFile(filename);

    printf("Cyphertext to decrypt: %s\n", known_ciphertext);

    baton_method(known_ciphertext, crib);
}
