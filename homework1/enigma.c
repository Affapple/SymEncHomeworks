// Simplified Enigma (no ring setting, etc.) for the homework

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

int rotor[3][26] = {
    // EKMFLGDQVZNTOWYHXUSPAIBRCJ
    {4,10,12,5,11,6,3,16,21,25,13,19,14,22,24,7,23,20,18,15,0,8,1,17,2,9}, // N
    // AJDKSIRUXBLHWTMCQGZNPYFVOE
    {0,9,3,10,18,8,17,20,23,1,11,7,22,19,12,2,16,6,25,13,15,24,5,21,14,4}, // M
    // BDFHJLCPRTXVZNYEIWGAKMUSQO
    {1,3,5,7,9,11,2,15,17,19,23,21,25,13,24,4,8,22,6,0,10,12,20,18,16,14}, // L
};

int rotor_inverse[3][26] = {
    {20,22,24,6,0,3,5,15,21,25,1,4,2,10,12,19,7,23,18,11,17,8,13,16,14,9},
    {0,9,15,2,25,22,17,11,5,1,3,10,14,19,24,20,16,6,4,13,7,23,12,8,21,18},
    {19,0,6,1,15,2,18,3,16,4,20,5,21,13,25,7,24,8,23,9,22,11,17,10,14,12},
};

int reflector[26] = \
    {5,21,15,9,8,0,14,24,4,3,17,25,23,22,6,2,19,10,20,16,18,1,13,12,7,11}
;

/* turn points of the rotors (notches) / empty ring setting */
int notch[3] = {16,4,21}; // QEV

/* plugboard */
int plugmap[26] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25};

int to_int(char c) {
    return toupper(c) - 'A';
}

void encrypt(char *key, char *plugboard, char *msg) {
    // plugboard initialization
    {
        int i;
        for (i = 0; i < 26; i++) {
            plugmap[i] = i;
        }

        i = 0;
        while (plugboard[i]) {
            if (plugboard[i] == ' ') {
                i++;
                continue;
            }
            int a = to_int(plugboard[i]);
            int b = to_int(plugboard[i+1]);
            plugmap[a] = b;
            plugmap[b] = a;
            printf("set plug %d <-> %d\n", a, b);
            i += 2;
        }
    }

    // message key (rotors state)
    int n_shift = to_int(key[0]);
    int m_shift = to_int(key[1]);
    int l_shift = to_int(key[2]);

    int i = 0;
    while (msg[i]) {
        // skip non-letters
        if (!(msg[i] >= 'A' && msg[i] <= 'Z')) {
            printf("%c", msg[i]);
            i++;
            continue;
        }

        int c = to_int(msg[i]);

        int p1 = 1, p2 = 0, p3 = 0;
        if (n_shift == notch[0]) p2 = 1;
        if (m_shift == notch[1]) p3 = p2 = 1;
        
        // printf("state %c%c%c\n", 'A'+n_shift, 'A'+m_shift, 'A'+l_shift);

        if (p1) n_shift = (n_shift + 1) % 26;
        if (p2) m_shift = (m_shift + 1) % 26;
        if (p3) l_shift = (l_shift + 1) % 26;

        // plugboard
        c = plugmap[c];

        /* ROTOR1 */
        c = (c + n_shift) % 26;
        c = rotor[0][c];
        c = (c - n_shift + 26) % 26;

        /* ROTOR2 */
        c = (c + m_shift) % 26;
        c = rotor[1][c];
        c = (c - m_shift + 26) % 26;


        /* ROTOR3 */
        c = (c + l_shift) % 26;
        c = rotor[2][c];
        c = (c - l_shift + 26) % 26;

        /* REFLECTOR */
        c = reflector[c];

        /* ROTOR3 */
        c = (c + l_shift) % 26;
        c = rotor_inverse[2][c];
        c = (c - l_shift + 26) % 26;

        /* ROTOR2 */
        c = (c + m_shift) % 26;
        c = rotor_inverse[1][c];
        c = (c - m_shift + 26) % 26;

        /* ROTOR1 */
        c = (c + n_shift) % 26;
        c = rotor_inverse[0][c];
        c = (c - n_shift + 26) % 26;

        // plugboard
        c = plugmap[c] ;


        printf("%c", 'A' + c);
        i++;
    }
    printf("\n");

}

int main2(int argc, char *argv[]) {
    char *pt = "FORAREASONHAPPENSEVERYTHING";
    char *key = "ABC";
    char *plug = "FX CR";
    // char *plug = "";
    
    encrypt(key, plug, pt);
    // should print: ZXFMKDPIGWPEFIFMZUPAXJXRCZV
    return 0;
}
