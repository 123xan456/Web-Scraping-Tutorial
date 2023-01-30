from ScrapeUtils import enter_IC

"""
Generate possible Malaysian IC numbers. Split by dd-mm-yy-pb-lastfour 
"""


def generate_IC(ckpt):
    ckpt_yy = int(ckpt[0:2].lstrip("0"))
    ckpt_mm = int(ckpt[2:4].lstrip("0"))
    ckpt_dd = int(ckpt[4:6].lstrip("0"))
    ckpt_pb = int(ckpt[6:8].lstrip("0"))
    ckpt_lf = int(ckpt[8:12].lstrip("0"))

    # first 6, DDMMYY from 1975 - 2005
    # month
    for month in range(ckpt_mm, 13):

        mm = f"{month:02d}"
        odd_months = ["04", "06", "09", "11"]  # 30 days

        if mm in odd_months:
            days = 30
        elif mm == "02":
            days = 28
        else:
            days = 31

        for day in range(ckpt_dd, days + 1):

            dd = f"{day:02d}"

            for year in range(ckpt_yy, 99):  # 1975-1999

                yymmdd = str(year) + mm + dd

                # next 2, labeled as PB(place of birth), numbers 17-20 not included
                for PB in range(ckpt_pb, 60):

                    non_PB = [17, 18, 19, 20]
                    if PB in non_PB:
                        continue

                    pb = f"{PB:02d}"

                    # last 4
                    for lfour in range(ckpt_lf, 10000):
                        lf = f"{lfour:04d}"

                        IC = yymmdd + pb + lf
                        enter_IC(IC)
                        with open("Res/ckpt.txt", "w") as checkpoint:
                            checkpoint.write(IC)

            for year in range(ckpt_yy, 6):  # 2000-2006

                dd = f"{year:02d}"

                yymmdd = str(year) + mm + dd

                # next 2, labeled as PB(place of birth), numbers 17-20 not included
                for PB in range(ckpt_pb, 60):

                    non_PB = [17, 18, 19, 20]
                    if PB in non_PB:
                        continue

                    pb = f"{PB:02d}"

                    # last 4
                    for lfour in range(ckpt_lf, 10000):
                        lf = f"{lfour:04d}"

                        IC = yymmdd + pb + lf
                        enter_IC(IC)
                        with open("Res/ckpt.txt", "w") as checkpoint:
                            checkpoint.write(IC)
