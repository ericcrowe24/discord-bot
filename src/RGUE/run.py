from RGUE import main
import sys

if sys.argv[1] == "-init" or sys.argv[1] == "-i":
    main(sys.argv[2], True, host=sys.argv[3], user=sys.argv[4], password=sys.argv[5], database=sys.argv[6])
else:
    main(sys.argv[1], host=sys.argv[2], user=sys.argv[3], password=sys.argv[4], database=sys.argv[5])
