from Crypto.Util.number import long_to_bytes, bytes_to_long
from gmpy2 import iroot

# part 1
e1 = 65537
p1 = 152933908726088000025981821717328900253841375038873501148415965946834656401640031351528841350980891403699057384028031438869081577476655254545307973436745130347696405243778481262922512227444915738801835842194123487258255790292004204412236314558718035967575479232723997430178018130995420315759809636522091902529
q1 = 173403581892981708663967289381727914513043623656015065332774927693090954681172215632003125824638611519248812013286298011144213434368768979531792528759533473573346156338400142951284462417074992959330154930806611253683603690442142765076944118447174491399811297223146324861971722035746276165056022562961558299229
ct1 = 24900222896050719055946861973957246283663114493271057619080357155524140641110166671081924849912377863714741017586072836978357770860853088772671413685690588862677870057778743649753806625109141461870634890427341765490174013453580041222600439459744928592280825572907034701116518706347830413085865254963646096687533779205345001529893651672061316525244476464884343232361498032095529980932018530224029715267731845742371944443150142380656402289372470902457020777826323051802030062577945893807552316343833971210833255536637260838474638607847822451324479398241526919184038034180388382949827367896808363560947298749154349868503

phi1 = (p1 - 1)*(q1 - 1)
d1 = pow(e1, -1, phi1)
flag1 = long_to_bytes(pow(ct1, d1, p1*q1))

e2 = 3
n2 = 17832697294201997154036617011957221780954165482288666773904510458098283881743910060438108775052144170769164876758249100567442926826366952851643073820832317493086415304740069439166953466125367940677570548218324219386987869433677168670642103353927101790341856159406926994785020050276564014860180970395749578442970075496442876475883003906961049702649859496118324912885388643549649071478725024867410660900848046927547400320456993982744075508818567475254504481562096763749301743619222457897353143558783627148704136084952125284873914605708215421331001883445600583624655438154001230490220705092656548338632165583188199066759
ct2 = 55717486909410107003108426413232346564412491530111436942121941739686926249314710854996834619
flag2 = long_to_bytes(iroot(ct2, 3)[0])

e3 = 65537
n3 = 107710970774233
ct3 = [18128889449669, 12202311999558, 10705744036504, 23864757944740]

# part 3: http://factordb.com/index.php?query=107710970774233
p3, q3 = 8885719, 12121807
phi3 = (p3 - 1) * (q3 - 1)
d3 = pow(e3, -1, phi3)
flag3 = b''
for ct in ct3:
    flag3 += long_to_bytes(pow(ct, d3, n3))
print(flag1 + flag2 + flag3)