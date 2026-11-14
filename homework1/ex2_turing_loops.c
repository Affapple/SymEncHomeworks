#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "./enigma.c"
#include "./utils.c"

#define max(a, b) (a > b ? a : b)
#define to2dArrIdx(x, y, dim) (y*dim + x)

typedef struct {
    int n_shift;
    int m_shift;
    int l_shift;
} EnigmaState;

EnigmaState* getEnigmaAt(int n_shift, int m_shift, int l_shift) {
    EnigmaState* machine = (EnigmaState*) malloc(sizeof(EnigmaState));
    machine->n_shift = n_shift;
    machine->m_shift = m_shift;
    machine->l_shift = l_shift;
    return machine;
}

EnigmaState** getEnigmaStates(int* initialKey, int biggestState) {
    int n_shift = initialKey[0];
    int m_shift = initialKey[1];
    int l_shift = initialKey[2];

    int i = 0;
    EnigmaState** machines = (EnigmaState **) calloc(biggestState+1, sizeof(EnigmaState*));
    while (i <= biggestState) {
        // First get machine pre encryption
        EnigmaState* machine = getEnigmaAt(n_shift, m_shift, l_shift);
        machines[i] = machine;

        // Then update parameters to the next machine
        int p1 = 1, p2 = 0, p3 = 0;
        if (n_shift == notch[0]) p2 = 1;
        if (m_shift == notch[1]) p3 = p2 = 1;
        
        if (p1) n_shift = (n_shift + 1) % 26;
        if (p2) m_shift = (m_shift + 1) % 26;
        if (p3) l_shift = (l_shift + 1) % 26;
    
        i++;
    }

    return machines;
}

int getEncryptedLetted(int letter, EnigmaState* machine) {
    int c = letter;

    int n_shift = machine->n_shift;
    int m_shift = machine->m_shift;
    int l_shift = machine->l_shift;

    int p1 = 1, p2 = 0, p3 = 0;
    if (n_shift == notch[0]) p2 = 1;
    if (m_shift == notch[1]) p3 = p2 = 1;
    
    if (p1) n_shift = (n_shift + 1) % 26;
    if (p2) m_shift = (m_shift + 1) % 26;
    if (p3) l_shift = (l_shift + 1) % 26;

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


    return c;
}

typedef struct {
    int* chainPath;
    int chainSize;
    char initialLetter;
} Chain;

Chain** initializeLoops() {
    Chain** loops = calloc(4, sizeof(Chain*));

    loops[0] = (Chain*) calloc(1, sizeof(Chain));
    loops[1] = (Chain*) calloc(1, sizeof(Chain));
    loops[2] = (Chain*) calloc(1, sizeof(Chain));

    /* Loop: V -7-> T -3-> J -2-> Z -1-> V */
    loops[0]->chainPath = malloc(4*sizeof(int));
    loops[0]->chainPath[0] = 7; loops[0]->chainPath[1]=3; loops[0]->chainPath[2] = 2; loops[0]->chainPath[3]=1;
    loops[0]->chainSize = 4;
    loops[0]->initialLetter = to_int('V');

    /* Loop: V -4-> Z -1-> V */
    loops[1]->chainPath = malloc(2*sizeof(int));
    loops[1]->chainPath[0] = 4; loops[1]->chainPath[1]=1;
    loops[1]->chainSize = 2;
    loops[1]->initialLetter = to_int('V');

    /* Loop: V -7-> T -12-> J -2-> Z -1-> V */
    loops[2]->chainPath = malloc(4*sizeof(int));
    loops[2]->chainPath[0] = 7; loops[2]->chainPath[1]=12;
    loops[2]->chainPath[2] = 2; loops[2]->chainPath[3]=1;
    loops[2]->chainSize = 4;
    loops[2]->initialLetter = to_int('V');
    return loops;
}

void turing_loops(Chain** loops, int numLoops, int numStates) {
    for (int rotor3 = to_int('A'); rotor3 <= to_int('Z'); rotor3++) {
        for (int rotor2 = to_int('A'); rotor2 <= to_int('Z'); rotor2++) {
            for (int rotor1 = to_int('A'); rotor1 <= to_int('Z'); rotor1++) {
                int key[3] = {rotor1, rotor2, rotor3};
                EnigmaState** machines = getEnigmaStates(
                    key,
                    numStates
                );

                char possiblePlugboardConfig[26*26];
                memset(possiblePlugboardConfig, 1, 26*26);
                for (int loopsIdx = 0; loopsIdx<numLoops; loopsIdx++) {
                    Chain* loop = loops[loopsIdx];
                    int initialLetter = loop->initialLetter;

                    for (size_t cv = to_int('A'); cv <= to_int('Z'); cv++) {
                        EnigmaState* machine = NULL;
                        int encrypted = cv;
                        for(int i=0; i < loop->chainSize; i++) {
                            machine = machines[loop->chainPath[i]-1];
                            encrypted = getEncryptedLetted(encrypted, machine);
                        }

                        if (encrypted != cv) {
                            int arrayIndex = to2dArrIdx(cv, initialLetter, 26);
                            int revArrayIndex = to2dArrIdx(initialLetter, cv, 26);
                            possiblePlugboardConfig[arrayIndex] = 0;
                            possiblePlugboardConfig[revArrayIndex] = 0;
                        }
                    }
                }

                int anyValid = 0;
                for (int loopsIdx = 0; loopsIdx < numLoops; loopsIdx++) {
                    int initialLetter = loops[loopsIdx]->initialLetter;
                    for (int cv = to_int('A'); cv <= to_int('Z'); cv++) {
                        int arrayIndex = to2dArrIdx(initialLetter, cv, 26);
                        if (possiblePlugboardConfig[arrayIndex] == 1) {
                            anyValid = 1;
                            break;
                        }
                    }
                    if (anyValid) break;
                }
                if (!anyValid) continue;

                char a = 'A' + rotor1;
                char b = 'A' + rotor2;
                char c = 'A' + rotor3;
                printf("Potential key: %c%c%c;\t", a,b,c);

                int visited[26] = {[0 ... 25] = 0};
                for (int loopsIdx = 0; loopsIdx<numLoops; loopsIdx++) {
                    Chain* loop = loops[loopsIdx];
                    int initialLetter = loop->initialLetter;

                    if (visited[initialLetter]) {
                        continue;
                    }

                    visited[initialLetter] = 1;

                    char loopLetter = 'A' + initialLetter;
                    printf("Possible plugboard config for C(%c) = ", loopLetter);
                    for (int idxLetter = to_int('A'); idxLetter <= to_int('Z'); idxLetter++) {
                        int arrayIndex = to2dArrIdx(initialLetter, idxLetter, 26);
                        if (possiblePlugboardConfig[arrayIndex] == 1) {
                            printf("%c, ", 'A' + idxLetter);
                        }
                    }
                    printf("\n");
                }
            }
        }
    }
    // Memory cleanup is left as an exercise to the reader
}

int main(void) {
    /**
    * We know that
    * R7 R3 R2 R1 C(V) = C(V)
    * R4 R1 C (V) = C(V)
    * R7 R3 R12 R8 C(V) = C(V)
    *
    * With 2 loops we expect to have one false positive every 26^2 configs
    * With 3 loops we expect to have one false positive every 26^3 configs
    * With 4 loops we expect to have one false positive every 26^4 (I believe) configs
    **/

    int NUM_LOOPS = 3;
    int MAX_STATE = 12;
    turing_loops(initializeLoops(), NUM_LOOPS, MAX_STATE);
    exit(EXIT_SUCCESS);
}
