import pysftp, sys, os

# Dictionary containing the different folder types:
folder_types = { 'ag': "Agenda's",
                 'ah': 'Kamervragen met antwoorden (Aanhangsels)',
                 'blg': 'Bijlagen',
                 'h': 'Handelingen',
                 'kst': 'Kamerstukken',
                 'kv': 'Kamervragen zonder antwoorden',
                 'nds': 'Niet-dossierstukken',
                 'stb': 'Staatsblad',
                 'stcrt': 'Staatscourant',
                 'trb': 'Tractatenblad'}

def list_contents(x, ftype):
    """List all the xml files in the file tree descendants of the current folder.
    By default only list xml files from the 'ah' folder."""
    
    def get_contents(x, folder, ftype):
        """Get the contents of a particular folder.
        Returns files and folders as separate sets."""
        oldpwd  = x.pwd
        x.cwd(folder)
        pwd     = x.pwd
        files   = set()
        folders = set()
        for item in x.listdir():
            if x.isdir(item):
                if item.isdigit() or item.startswith(ftype):
                    folders.add(pwd + item)
            else:
                # Add the file to the set of files if it is a content-bearing xml file.
                if item.endswith('.xml') and not 'metadata' in item and not 'changelog' in item:
                    files.add(pwd + item)
        x.cwd(oldpwd)
        return files, folders
    
    # Initialize the files and todo sets.
    files, todo = get_contents(x, x.pwd, ftype)
    
    # And let's dig through the folders using a while loop. The todo list will eventually
    # be empty when there are no more (sub)folders to examine.
    while not len(todo) == 0:
        # get the contents of the next folder:
        current   = todo.pop()
        new_files, new_folders = get_contents(x, current, ftype)
        
        # and update our knowledge:
        files.update(new_files)
        todo.update(new_folders)
    return files

def store_locally(x,filename,targetfolder='./xmlfiles/'):
    with x.open(filename) as f_source:
        filename = filename.split('/')[-1]
        with open(targetfolder + filename, 'w') as f_target:
            f_target.write(f_source.read())

def store_files_for_year(year, ftype, verbose=False):
    x = pysftp.Connection('bestanden.officielebekendmakingen.nl',
                          username='anonymous',
                          password='secret')
    x.cwd(year)
    for filename in list_contents(x, ftype):
        path = '../data/' + ftype + '/' + year + '/'
        if not os.path.exists(path):
            os.makedirs(path)
        store_locally(x,filename, targetfolder=path)
        if verbose:
            print 'Copied file '+ filename

# Call this file with a particular year and, optionally, a folder type
# e.g. python overheid_sftp.py 2014 ah

if __name__ == "__main__":
    # Determine folder type (optional):
    if len(sys.argv) == 3:
        ftype = sys.argv[2].lower()
        if not ftype in folder_types:
            raise KeyError('Folder type does not exist!')
    else:
        ftype = 'ah'
    
    # Determine year:
    year = sys.argv[1]
    if year.isdigit():
        print "Searching for files from the year", year
        print "These files are: " + folder_types[ftype]
        
        store_files_for_year(year, ftype, verbose=False)
    else:
        raise ValueError("Only digits allowed; call this file with a year!")
