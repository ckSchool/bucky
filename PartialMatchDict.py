class PartialMatchDict(dict):
    """
    A dictionary structure that will return a value if its key at least partially uniquely matches a passed-in key.
    Exact matches returned first, then checks for partial matches to the beginnings of keys while ignoring case.
    Example:
    >>> pd = PartialMatchDict()
    >>> pd["thelongstring"] = 1
    >>> pd["the"] = 2
    >>> pd["TheString"] = 3
    
    >>> pd["thelongstr"]
    1
    >>> pd["the"]
    2
    >>> pd["thestring"]
    3
    >>> pd["th"]
    KeyError: "Partial key 'th' not unique"
    >>> pd["anotherstring"]
    KeyError: "Missing key 'anotherstring'"
    """

    def __init__(self, items = None):
        super(PartialMatchDict, self).__init__()

        if items:
            self.update(items)

    # PartialSearch - Do the partial search.
    # param: partialKey = key to try to match.
    # returns: a tuple, 0th element is True if found a value, None if no possible match, False if no unique match was found;
    #                   1st element indicates value if successful, or first possible value if not unique.
    def PartialSearch(self, partialKey):
        # if the item is in the dictionary then just return it
        if dict.__contains__(self, partialKey):
            return (True, dict.__getitem__(self, partialKey))

        matchFound = (None, None)
        # Don't partial match an empty string, because it will match anything.
        if len(partialKey) == 0:
            # "" is not a unique key.
            return (False, "(empty string)")
        # See if any key starts with our partialKey.  Use lower() to ignore case.
        lowerPartialKey = str(partialKey).lower()
        for key in self:
            if str(key).lower().startswith(lowerPartialKey):
                if not matchFound[0]:
                    matchFound = (True, dict.__getitem__(self, key))
                else:
                    # More than one potential match, so set our success indicator to False.
                    matchFound = (False, matchFound[1])
                    break
        return matchFound

    # Find out if we have an exact key in the set.
    def has_exact_key(self, item):
        return dict.__contains__(self, item)

    # Override dict method, used for "in" operator.
    def __contains__(self, item):
        # Compare to True to have None (not found at all) returns False.
        return (self.PartialSearch(item)[0] == True)

    # Override dict method, used when looking up key using [].
    def __getitem__(self, item):
        wasFound, theValue = self.PartialSearch(item)
        if not wasFound:
            errorMsg = "%s"
            if wasFound == None:
                # Couldn't find anything at all.
                errorMsg = "Missing key '%s'"
            else:
                # Key not unique
                errorMsg = "Partial key '%s' not unique"
            raise KeyError(errorMsg % (str(item)))
        else:
            return theValue

# If we run the file from the command prompt, do some tests.
if __name__ == '__main__':
    testdict = PartialMatchDict()
    print "** Assigning testdict['Primary'] = 1"
    testdict['Primary'] = 1
    print "** Assigning testdict['Secondary'] = 2"
    testdict['Secondary'] = 2
    print "** Assigning testdict['Tertiary'] = 3"
    testdict['Tertiary'] = 3
    print "** Assigning testdict['thirtieth'] = 30"
    testdict['thirtieth'] = 30

    # Make sure we find what we expect.
    print "testdict['Primary'] == ", testdict['Primary']
    print "testdict['primary'] == ", testdict['primary']
    print "testdict['secondary'] == ", testdict['secondary']
    print "testdict['tertiary'] == ", testdict['tertiary']
    print "testdict['tert'] == ", testdict['tert']
    print "testdict['thirtieth'] == ", testdict['thirtieth']
    print "testdict['thirt'] == ", testdict['thirt']
    print "testdict['th'] == ", testdict['th']
    print "** Assigning testdict['th'] = None"
    testdict['th'] = None
    print "testdict['th'] == ", testdict['th']
    print "testdict['thirt'] == ", testdict['thirt']

    # Expect some errors.
    try:
        print testdict['quart']
    except KeyError:
        print "There is no possible match, so could not find testdict['quart']"
    try:
        print testdict['t']
    except KeyError:
        print "Possible matches are not unique, so could not find testdict['t']"