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
    int fromLetter;
    int stateIdx;
    int toLetter;
} MenuLink;

typedef struct {
    MenuLink* links; /* fromLetter --stateIdx--> toLetter */
    int chainSize;
    char initialLetter;
    int isLoop;
} Chain;

Chain** initializeChains() {
    Chain** chains = calloc(9, sizeof(Chain*));

    chains[0] = (Chain*) calloc(1, sizeof(Chain));
    chains[1] = (Chain*) calloc(1, sizeof(Chain));
    chains[2] = (Chain*) calloc(1, sizeof(Chain));
    chains[3] = (Chain*) calloc(1, sizeof(Chain));
    chains[4] = (Chain*) calloc(1, sizeof(Chain));
    chains[5] = (Chain*) calloc(1, sizeof(Chain));
    chains[6] = (Chain*) calloc(1, sizeof(Chain));
    chains[7] = (Chain*) calloc(1, sizeof(Chain));

    /* Loop: V --7--> T --3--> J --2--> Z --1--> V */
    chains[0]->links = malloc(4*sizeof(MenuLink));
    chains[0]->links[0] = (MenuLink){to_int('V'), 7,  to_int('T')};
    chains[0]->links[1] = (MenuLink){to_int('T'), 3,  to_int('J')};
    chains[0]->links[2] = (MenuLink){to_int('J'), 2,  to_int('Z')};
    chains[0]->links[3] = (MenuLink){to_int('Z'), 1,  to_int('V')};
    chains[0]->chainSize = 4;
    chains[0]->initialLetter = to_int('V');
    chains[0]->isLoop = 1;

    /* Loop: V --4--> Z --1--> V */
    chains[1]->links = malloc(2*sizeof(MenuLink));
    chains[1]->links[0] = (MenuLink){to_int('V'), 4,  to_int('Z')};
    chains[1]->links[1] = (MenuLink){to_int('Z'), 1,  to_int('V')};
    chains[1]->chainSize = 2;
    chains[1]->initialLetter = to_int('V');
    chains[1]->isLoop = 1;

    /* Loop: V --7--> T --12--> J --2--> Z --1--> V */
    chains[2]->links = malloc(4*sizeof(MenuLink));
    chains[2]->links[0] = (MenuLink){to_int('V'), 7,  to_int('T')};
    chains[2]->links[1] = (MenuLink){to_int('T'), 12, to_int('J')};
    chains[2]->links[2] = (MenuLink){to_int('J'), 2,  to_int('Z')};
    chains[2]->links[3] = (MenuLink){to_int('Z'), 1,  to_int('V')};
    chains[2]->chainSize = 4;
    chains[2]->initialLetter = to_int('V');
    chains[2]->isLoop = 1;

    /* Chain: P --10--> C --6--> Z */
    chains[3]->links = malloc(2*sizeof(MenuLink));
    chains[3]->links[0] = (MenuLink){to_int('P'), 10, to_int('C')};
    chains[3]->links[1] = (MenuLink){to_int('C'), 6,  to_int('Z')};
    chains[3]->chainSize = 2;
    chains[3]->initialLetter = to_int('P');
    chains[3]->isLoop = 0;

    /* Chain: I --9--> T */
    chains[4]->links = malloc(1*sizeof(MenuLink));
    chains[4]->links[0] = (MenuLink){to_int('I'), 9,  to_int('T')};
    chains[4]->chainSize = 1;
    chains[4]->initialLetter = to_int('I');
    chains[4]->isLoop = 0;

    /* Chain: O --13--> F */
    chains[5]->links = malloc(1*sizeof(MenuLink));
    chains[5]->links[0] = (MenuLink){to_int('O'), 13, to_int('F')};
    chains[5]->chainSize = 1;
    chains[5]->initialLetter = to_int('O');
    chains[5]->isLoop = 0;

    /* Chain: R --14--> B */
    chains[6]->links = malloc(1*sizeof(MenuLink));
    chains[6]->links[0] = (MenuLink){to_int('R'), 14, to_int('B')};
    chains[6]->chainSize = 1;
    chains[6]->initialLetter = to_int('R');
    chains[6]->isLoop = 0;

    /* Chain: G --11--> U --5--> S */
    chains[7]->links = malloc(2*sizeof(MenuLink));
    chains[7]->links[0] = (MenuLink){to_int('G'), 11, to_int('U')};
    chains[7]->links[1] = (MenuLink){to_int('U'), 5,  to_int('S')};
    chains[7]->chainSize = 2;
    chains[7]->initialLetter = to_int('G');
    chains[7]->isLoop = 0;

    return chains;
}

void turing_welchman(Chain** loops, int numLoops, int numStates) {
    // Collect all unique menu links across all loops
    int maxLinks = 0;
    for (int i = 0; i < numLoops; i++) maxLinks += loops[i]->chainSize;
    MenuLink* allLinks = malloc(maxLinks * sizeof(MenuLink));
    int numLinks = 0;
    for (int i = 0; i < numLoops; i++) {
        for (int j = 0; j < loops[i]->chainSize; j++) {
            MenuLink ml = loops[i]->links[j];
            int found = 0;
            for (int k = 0; k < numLinks; k++) {
                if (allLinks[k].fromLetter == ml.fromLetter &&
                    allLinks[k].stateIdx   == ml.stateIdx   &&
                    allLinks[k].toLetter   == ml.toLetter) { found = 1; break; }
            }
            if (!found) allLinks[numLinks++] = ml;
        }
    }

    // Collect all unique node letters that appear in the menu (for output)
    int menuNodes[26] = {0};
    for (int i = 0; i < numLinks; i++) {
        menuNodes[allLinks[i].fromLetter] = 1;
        menuNodes[allLinks[i].toLetter]   = 1;
    }

    for (int rotor3 = to_int('A'); rotor3 <= to_int('Z'); rotor3++) {
        for (int rotor2 = to_int('A'); rotor2 <= to_int('Z'); rotor2++) {
            for (int rotor1 = to_int('A'); rotor1 <= to_int('Z'); rotor1++) {
                int key[3] = {rotor1, rotor2, rotor3};
                EnigmaState** machines = getEnigmaStates(key, numStates);

                // possible[letter][cv] == 1  means "C(letter) = cv is still possible"
                char possible[26*26];
                memset(possible, 1, 26*26);

                // Loop-closure initial elimination:
                // for each loop, test all 26 values for C(initialLetter).
                // If the full chain doesn't map cv back to cv, eliminate it.
                for (int loopsIdx = 0; loopsIdx < numLoops; loopsIdx++) {
                    Chain* loop = loops[loopsIdx];
                    if (!loop->isLoop) continue;
                    int initialLetter = loop->initialLetter;
                    for (int cv = to_int('A'); cv <= to_int('Z'); cv++) {
                        int encrypted = cv;
                        for (int i = 0; i < loop->chainSize; i++) {
                            encrypted = getEncryptedLetted(encrypted, machines[loop->links[i].stateIdx - 1]);
                        }
                        if (encrypted != cv) {
                            possible[to2dArrIdx(cv, initialLetter, 26)] = 0;
                            possible[to2dArrIdx(initialLetter, cv, 26)] = 0;
                        }
                    }
                }

                /* Welchman diagonal board: propagate through every menu link in both directions.
                 *
                 * Each link  A -state-> B  encodes the constraint:
                 *   C(A) = x => enc(x, machine) = C(B)
                 * And in reverse
                 *
                 * C(A)=x <=> C(x)=A
                 * so we eliminate both possible[A][x] and possible[x][A].
                 *
                 * We iterate until no new eliminations occur. 
                 **/
                int changed = 1;
                while (changed) {
                    changed = 0;
                    for (int li = 0; li < numLinks; li++) {
                        int A = allLinks[li].fromLetter;
                        int B = allLinks[li].toLetter;
                        EnigmaState* machine = machines[allLinks[li].stateIdx - 1];

                        // Forward: C(A) = x => C(B) = enc(x)
                        for (int x = 0; x < 26; x++) {
                            if (!possible[to2dArrIdx(x, A, 26)]) continue;
                            int y = getEncryptedLetted(x, machine);
                            if (!possible[to2dArrIdx(y, B, 26)]) {
                                possible[to2dArrIdx(x, A, 26)] = 0;
                                possible[to2dArrIdx(A, x, 26)] = 0;  // symmetry
                                changed = 1;
                            }
                        }

                        // Backward: C(B) = y => C(A) = enc(y)
                        for (int y = 0; y < 26; y++) {
                            if (!possible[to2dArrIdx(y, B, 26)]) continue;
                            int x = getEncryptedLetted(y, machine);
                            if (!possible[to2dArrIdx(x, A, 26)]) {
                                possible[to2dArrIdx(y, B, 26)] = 0;
                                possible[to2dArrIdx(B, y, 26)] = 0;  // symmetry
                                changed = 1;
                            }
                        }
                    }
                }

                // Only save if every menu node still has at least one valid option
                int allNodesValid = 1;
                for (int node = 0; node < 26; node++) {
                    int nodeHasOption = 0;
                    if (!menuNodes[node]) continue;
                    for (int cv = 0; cv < 26; cv++) {
                        if (possible[to2dArrIdx(cv, node, 26)]) {
                            nodeHasOption = 1;
                            break;
                        }
                    }
                    if (!nodeHasOption) {
                        allNodesValid = 0;
                        break;
                    }
                }
                if (!allNodesValid) continue;

                char a = 'A' + rotor1;
                char b = 'A' + rotor2;
                char c = 'A' + rotor3;
                printf("Potential key: %c%c%c\n", a, b, c);

                // Print possible plugboard values for every menu node
                for (int node = 0; node < 26; node++) {
                    if (!menuNodes[node]) continue;
                    printf("  C(%c) = ", 'A' + node);
                    for (int cv = 0; cv < 26; cv++) {
                        if (possible[to2dArrIdx(cv, node, 26)]) {
                            printf("%c ", 'A' + cv);
                        }
                    }
                    printf("\n");
                }
            }
        }
    }
}

int main(void) {
    int NUM_LOOPS = 8;
    int MAX_STATE = 14;
    turing_welchman(initializeChains(), NUM_LOOPS, MAX_STATE);
    exit(EXIT_SUCCESS);
}
