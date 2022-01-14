if __name__ == "__main__":
    from AbstractProfile import AbstractProfile
else:
    from TestStandProfiles.AbstractProfile import AbstractProfile
### DO NOT EDIT ABOVE ###

class TestStandBehaviour(AbstractProfile):
    pass

### DO NOT EDIT BELOW ###
if __name__ == "__main__":
    instance = TestStandBehaviour()
    instance.is_valid()