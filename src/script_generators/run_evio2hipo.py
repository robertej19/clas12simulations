def run_evio2hipo(scard,**kwargs):
  strn = """\nls -l
set evio2hipo_start = `date`
evio2hipo -r 11 -t {0} -s {1} -i out.ev -o gemc.hipo
echo after decoder\n""".format('scard.tcurrent','scard.pcurrent')
  return strn
