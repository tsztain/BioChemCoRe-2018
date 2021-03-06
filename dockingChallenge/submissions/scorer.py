import schrodinger.structure as SS
import schrodinger.structutils.analyze as SSUA
import glob

key ={"../encodedProteins/12.pdb":"scoring/1fkf-clean.pdb",
"../encodedProteins/13.pdb":"scoring/1ihi-clean.pdb",
"../encodedProteins/1.pdb":"scoring/1j8u-clean.pdb",
"../encodedProteins/2.pdb":"scoring/2p16-clean.pdb",
"../encodedProteins/3.pdb":"scoring/2w4x-clean.pdb",
"../encodedProteins/4.pdb":"scoring/3bjm-clean.pdb",
"../encodedProteins/5.pdb":"scoring/3d4s-clean.pdb",
"../encodedProteins/6.pdb":"scoring/3daz-clean.pdb",
"../encodedProteins/7.pdb":"scoring/3fhx-clean.pdb",
"../encodedProteins/8.pdb":"scoring/3n23-clean.pdb",
"../encodedProteins/9.pdb":"scoring/3nos-clean.pdb",
"../encodedProteins/10.pdb":"scoring/3nya-clean.pdb",
"../encodedProteins/11.pdb":"scoring/4lxz-clean.pdb"}
maekey ={"ss12.mae":"scoring/1fkf-clean.pdb",
"ss13.mae":"scoring/1ihi-clean.pdb",
"ss14.mae":"scoring/3n23-clean.pdb",
"ss01.mae":"scoring/1j8u-clean.pdb",
"ss02.mae":"scoring/2p16-clean.pdb",
"ss03.mae":"scoring/2w4x-clean.pdb",
"ss04.mae":"scoring/3bjm-clean.pdb",
"ss05.mae":"scoring/3d4s-clean.pdb",
"ss06.mae":"scoring/3daz-clean.pdb",
"ss07.mae":"scoring/3fhx-clean.pdb",
"ss08.mae":"scoring/3n23-clean.pdb",
"ss09.mae":"scoring/3nos-clean.pdb",
"ss10.mae":"scoring/3nya-clean.pdb",
"ss11.mae":"scoring/4lxz-clean.pdb"}
pdbKeys = {'ss12.mae':['1fkf','FK5'],
'ss13.mae':['1ihi','NAP'],
'ss14.mae':['3n23','OBN'],
'ss01.mae':['1j8u','H4B'],
'ss02.mae':['2p16','GG2'],
'ss03.mae':['2w4x','STZ'],
'ss03version_2.mae':['2w4x','STZ'],
'ss04.mae':['3bjm','BJM'],
'ss05.mae':['3d4s','TIM'],
'ss06.mae':['3daz','MZM'],
'ss07.mae':['3fhx','ATP'],
'ss08.mae':['3n23','OBN'],
'ss09.mae':['3nos','HAR'],
#'ss09.mae':['3nos','HEM'],
'ss10.mae':['3nya','JTZ'],
'ss11.mae':['4lxz','SHH']}
files = glob.glob('*mae')



for filename in files:
    print filename
    known = pdbKeys[filename]
    knownCpx = SS.StructureReader('scoring/'+known[0]+'.pdb').next()
    #print known.replace('-clean','Lig')
    #knownLig = SS.StructureReader(known.replace('-clean','Lig')).next()
    #print knownPtn, knownLig
    #knownCpx = knownPtn.merge(knownLig)
    #my_sw = SS.StructureWriter(known.replace('-clean.pdb','-complex.mae'))
    #my_sw.append(knownCpx)
    #my_sw.close()
    #searcher = SSUA.AslLigandSearcher()
    #searcher.search(knownCpx)
    #print searcher.getAsl()
    #within5 = SSUA.evaluate_asl(knownCpx,'fillres within 5 (%s) ' %(searcher.getAsl()))
    within5 = SSUA.evaluate_asl(knownCpx,'fillres within 5 (res.ptype "%s") ' %(known[1]))
    ligand = SSUA.evaluate_asl(knownCpx,'res.ptype "%s" ' %(known[1]))
    #print knownCpx.atom[ligand].smiles
    knownSet = set([str(knownCpx.atom[i].getResidue()) for i in within5])
    #print knownSet
    #1/0
    my_SR = SS.StructureReader(filename)
    guessSets = []
    #try:
    if 1:
        protein = my_SR.next()
        for i in range(3):
            #if 1:
            try:
                print 'ligand %i' %(i)
                ligand = my_SR.next()
                cpx = protein.merge(ligand)
                searcher = SSUA.AslLigandSearcher()
                searcher.search(cpx)
                #print searcher.getAsl()
                within5 = SSUA.evaluate_asl(cpx,'fillres within 5 (%s) ' %(searcher.getAsl()))
                guessSets.append(set([str(cpx.atom[i].getResidue()) for i in within5]))
                #ligAtoms = SSUA.evaluate_asl
            except:
                pass
    #except:
    #    pass
    for guessSet in guessSets:
        #print "Guess:", guessSet
        #print "Known:", knownSet
        print float(len(guessSet.intersection(knownSet)))/len(knownSet)
