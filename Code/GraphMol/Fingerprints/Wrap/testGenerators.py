from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
from rdkit.Chem import rdMHFPFingerprint
import unittest


class TestCase(unittest.TestCase):
    def setUp(self):
        pass

    def testMHFPFingerprint(self):
        s = "CN1C=NC2=C1C(=O)N(C(=O)N2C)C"
        t = "Cn1cnc2c1c(=O)[nH]c(=O)n2C"

        m = Chem.MolFromSmiles(s)
        enc = rdMHFPFingerprint.MHFPEncoder(128, 42)

        self.assertEqual(len(enc.CreateShinglingFromSmiles(s, rings=False)), 42)
        self.assertEqual(len(enc.CreateShinglingFromSmiles(s, min_radius=0)), 58)

        sh_a = enc.CreateShinglingFromSmiles(s)
        sh_b = enc.CreateShinglingFromMol(m)

        self.assertEqual(len(sh_a), 44)
        self.assertEqual(list(sh_a), list(sh_b))

        fp_a = enc.EncodeSmiles(s)
        fp_b = enc.EncodeMol(m)

        self.assertEqual(list(fp_a), list(fp_b))

        fp_c = enc.EncodeSmiles(t)
        dist = rdMHFPFingerprint.MHFPEncoder.Distance(fp_a, fp_c)
        self.assertEqual(dist, 0.2890625)

    def testAtomPairGenerator(self):
        m = Chem.MolFromSmiles("CCC")
        g = rdFingerprintGenerator.GetAtomPairGenerator()
        fp = g.GetSparseCountFingerprint(m)
        nz = fp.GetNonzeroElements()
        self.assertEqual(len(nz), 2)

        fp = g.GetCountFingerprint(m)
        nz = fp.GetNonzeroElements()
        self.assertEqual(len(nz), 2)

        fp = g.GetSparseFingerprint(m)
        nzc = fp.GetNumOnBits()
        self.assertEqual(nzc, 3)

        fp = g.GetFingerprint(m)
        nzc = fp.GetNumOnBits()
        self.assertEqual(nzc, 3)

        g = rdFingerprintGenerator.GetAtomPairGenerator(
            atomInvariantsGenerator=rdFingerprintGenerator.GetAtomPairAtomInvGen()
        )
        fp = g.GetSparseCountFingerprint(m)
        nz = fp.GetNonzeroElements()
        self.assertEqual(len(nz), 2)

        g = rdFingerprintGenerator.GetAtomPairGenerator(minDistance=2)
        fp = g.GetSparseCountFingerprint(m)
        nz = fp.GetNonzeroElements()
        self.assertEqual(len(nz), 1)

        g = rdFingerprintGenerator.GetAtomPairGenerator(maxDistance=1)
        fp = g.GetSparseCountFingerprint(m)
        nz = fp.GetNonzeroElements()
        self.assertEqual(len(nz), 1)

        g = rdFingerprintGenerator.GetAtomPairGenerator(useCountSimulation=False)
        fp = g.GetSparseFingerprint(m)
        nzc = fp.GetNumOnBits()
        self.assertEqual(nzc, 2)

        invGen = rdFingerprintGenerator.GetAtomPairAtomInvGen(includeChirality=False)
        invGenChirality = rdFingerprintGenerator.GetAtomPairAtomInvGen(
            includeChirality=True
        )
        g = rdFingerprintGenerator.GetAtomPairGenerator(
            includeChirality=False, atomInvariantsGenerator=invGen
        )
        gChirality = rdFingerprintGenerator.GetAtomPairGenerator(
            includeChirality=True, atomInvariantsGenerator=invGenChirality
        )
        fp = g.GetSparseCountFingerprint(m)
        nz = fp.GetNonzeroElements()
        fpChirality = gChirality.GetSparseCountFingerprint(m)
        nzChirality = fpChirality.GetNonzeroElements()
        self.assertNotEqual(nz.keys(), nzChirality.keys())

    def testMorganGenerator(self):
        m = Chem.MolFromSmiles("CCCCC")
        g = rdFingerprintGenerator.GetMorganGenerator(3)
        fp = g.GetSparseCountFingerprint(m)
        nz = fp.GetNonzeroElements()
        self.assertEqual(len(nz), 7)

    def testRDKitFPGenerator(self):
        m = Chem.MolFromSmiles("CCCCC")
        g = rdFingerprintGenerator.GetRDKitFPGenerator()
        fp = g.GetSparseCountFingerprint(m)
        nz = fp.GetNonzeroElements()
        self.assertEqual(len(nz), 4)

    def testTopologicalTorsionGenerator(self):
        m = Chem.MolFromSmiles("CCCCC")
        g = rdFingerprintGenerator.GetTopologicalTorsionGenerator()
        fp = g.GetSparseCountFingerprint(m)
        nz = fp.GetNonzeroElements()
        self.assertEqual(len(nz), 1)

    def testBulk(self):
        m1 = Chem.MolFromSmiles("CCC")
        m2 = Chem.MolFromSmiles("OCCCCC")
        m3 = Chem.MolFromSmiles("CCCCC")

        g = rdFingerprintGenerator.GetAtomPairGenerator()
        results = rdFingerprintGenerator.GetSparseCountFPs(
            [m1, m2, m3], rdFingerprintGenerator.AtomPairFP
        )
        self.assertEqual(results[0], g.GetSparseCountFingerprint(m1))
        self.assertEqual(results[1], g.GetSparseCountFingerprint(m2))
        self.assertEqual(results[2], g.GetSparseCountFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetMorganGenerator(2)
        results = rdFingerprintGenerator.GetSparseCountFPs(
            [m1, m2, m3], rdFingerprintGenerator.MorganFP
        )
        self.assertEqual(results[0], g.GetSparseCountFingerprint(m1))
        self.assertEqual(results[1], g.GetSparseCountFingerprint(m2))
        self.assertEqual(results[2], g.GetSparseCountFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetRDKitFPGenerator()
        results = rdFingerprintGenerator.GetSparseCountFPs(
            [m1, m2, m3], rdFingerprintGenerator.RDKitFP
        )
        self.assertEqual(results[0], g.GetSparseCountFingerprint(m1))
        self.assertEqual(results[1], g.GetSparseCountFingerprint(m2))
        self.assertEqual(results[2], g.GetSparseCountFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetTopologicalTorsionGenerator()
        results = rdFingerprintGenerator.GetSparseCountFPs(
            [m1, m2, m3], rdFingerprintGenerator.TopologicalTorsionFP
        )
        self.assertEqual(results[0], g.GetSparseCountFingerprint(m1))
        self.assertEqual(results[1], g.GetSparseCountFingerprint(m2))
        self.assertEqual(results[2], g.GetSparseCountFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetAtomPairGenerator()
        results = rdFingerprintGenerator.GetSparseFPs(
            [m1, m2, m3], rdFingerprintGenerator.AtomPairFP
        )
        self.assertEqual(results[0], g.GetSparseFingerprint(m1))
        self.assertEqual(results[1], g.GetSparseFingerprint(m2))
        self.assertEqual(results[2], g.GetSparseFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetMorganGenerator(2)
        results = rdFingerprintGenerator.GetSparseFPs(
            [m1, m2, m3], rdFingerprintGenerator.MorganFP
        )
        self.assertEqual(results[0], g.GetSparseFingerprint(m1))
        self.assertEqual(results[1], g.GetSparseFingerprint(m2))
        self.assertEqual(results[2], g.GetSparseFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetRDKitFPGenerator()
        results = rdFingerprintGenerator.GetSparseFPs(
            [m1, m2, m3], rdFingerprintGenerator.RDKitFP
        )
        self.assertEqual(results[0], g.GetSparseFingerprint(m1))
        self.assertEqual(results[1], g.GetSparseFingerprint(m2))
        self.assertEqual(results[2], g.GetSparseFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetTopologicalTorsionGenerator()
        results = rdFingerprintGenerator.GetSparseFPs(
            [m1, m2, m3], rdFingerprintGenerator.TopologicalTorsionFP
        )
        self.assertEqual(results[0], g.GetSparseFingerprint(m1))
        self.assertEqual(results[1], g.GetSparseFingerprint(m2))
        self.assertEqual(results[2], g.GetSparseFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetAtomPairGenerator()
        results = rdFingerprintGenerator.GetCountFPs(
            [m1, m2, m3], rdFingerprintGenerator.AtomPairFP
        )
        self.assertEqual(results[0], g.GetCountFingerprint(m1))
        self.assertEqual(results[1], g.GetCountFingerprint(m2))
        self.assertEqual(results[2], g.GetCountFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetMorganGenerator(2)
        results = rdFingerprintGenerator.GetCountFPs(
            [m1, m2, m3], rdFingerprintGenerator.MorganFP
        )
        self.assertEqual(results[0], g.GetCountFingerprint(m1))
        self.assertEqual(results[1], g.GetCountFingerprint(m2))
        self.assertEqual(results[2], g.GetCountFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetRDKitFPGenerator()
        results = rdFingerprintGenerator.GetCountFPs(
            [m1, m2, m3], rdFingerprintGenerator.RDKitFP
        )
        self.assertEqual(results[0], g.GetCountFingerprint(m1))
        self.assertEqual(results[1], g.GetCountFingerprint(m2))
        self.assertEqual(results[2], g.GetCountFingerprint(m3))
        self.assertEqual(len(results), 3)

        g = rdFingerprintGenerator.GetTopologicalTorsionGenerator()
        results = rdFingerprintGenerator.GetCountFPs(
            [m1, m2, m3], rdFingerprintGenerator.TopologicalTorsionFP
        )
        self.assertEqual(results[0], g.GetCountFingerprint(m1))
        self.assertEqual(results[1], g.GetCountFingerprint(m2))
        self.assertEqual(results[2], g.GetCountFingerprint(m3))
        self.assertEqual(len(results), 3)


if __name__ == "__main__":
    unittest.main()
