def checksum (id):
    id2="0"*(8-len(id))+id
    weights = [1, 2, 1, 2, 1, 2, 1, 2]
    check_sum=0
    for inx in range(0, len(id2)):
        mult=0
        mult=int(id2[inx])*weights[inx]
        mult=mult//10+mult%10

        check_sum+=mult
    mod_chs=check_sum%10
    ans=10-mod_chs
    ans=ans//10+ans%10
    print(ans)
checksum("123")