import os, subprocess
from app.SaveData import load_data, save_data

GLOVE_ZIPS = {
    "6B": "glove.6B.zip",
    "42B": "glove.42B.300d.zip",
    "840B": "glove.840B.300d.zip"
}

GLOVE_FILES = {
    "6B": {
        "50d": "glove.6B.50d.txt",
        "100d": "glove.6B.100d.txt",
        "200d": "glove.6B.200d.txt",
        "300d": "glove.6B.300d.txt",
    },
    "42B": {
        "300d": "glove.42B.300d.txt",
    },
    "840B": {
        "300d": "glove.840B.300d.txt",
    }
}

def get_possible_glove_models():
    combinations = []
    for tokens in GLOVE_FILES:
        for vectors in GLOVE_FILES[tokens]:
            combinations.append(f"{tokens} - {vectors}")
    return combinations

def get_downloaded_glove_models():
    downloaded = []
    for tokens in GLOVE_FILES:
        for vectors in GLOVE_FILES[tokens]:
            if glove_installed(tokens, vectors):
                downloaded.append({
                    "tokens": tokens,
                    "vectors": vectors
                })
    return downloaded

def check_zip_exists(tokens):
    if tokens not in GLOVE_FILES:
        raise ValueError(f"Invalid glove tokens: {tokens}")
    
    return os.path.exists("./Code/" + GLOVE_ZIPS[tokens])

# Checks if a GloVe file already exists
def check_glove_exists():
    glove_files = [f for f in os.listdir("./Code/") if f.startswith("glove") and f.endswith(".txt")]
        
    if len(glove_files) > 0:
        return glove_files[0]
    else:
        return None

def check_glove_downloaded(tokens):
    if tokens not in GLOVE_FILES:
        raise ValueError(f"Invalid glove tokens: {tokens}")
    
    for vectors in GLOVE_FILES[tokens]:
        if glove_installed(tokens, vectors):
            return True
    return False

# Checks for a specific GloVe file
def glove_installed(tokens, vectors):
    if tokens not in GLOVE_FILES:
        raise ValueError(f"Invalid glove tokens: {tokens}")
    
    if vectors not in GLOVE_FILES[tokens]:
        raise ValueError(f"Invalid glove vectors: {vectors}")
    
    return os.path.exists("./Code/" + GLOVE_FILES[tokens][vectors])



def download_glove_model(tokens = next(iter(GLOVE_ZIPS))):
    if tokens not in GLOVE_ZIPS:
        raise ValueError(f"Invalid glove tokens: {tokens}")
    
    print("Downloading GloVe from: http://nlp.stanford.edu/data/" + GLOVE_ZIPS[tokens])
    subprocess.check_call(["wget", "http://nlp.stanford.edu/data/" + GLOVE_ZIPS[tokens], "-P", "./Code/"])



def extract_glove_model(tokens = next(iter(GLOVE_ZIPS))):
    if tokens not in GLOVE_FILES:
        raise ValueError(f"Invalid glove tokens: {tokens}")
    
    if not os.path.exists("./Code/" + GLOVE_ZIPS[tokens]):
        raise FileNotFoundError(f"Missing GloVe zip file: {GLOVE_ZIPS[tokens]}")

    print("Extracting GloVe: " + GLOVE_ZIPS[tokens])
    subprocess.check_call(["unzip", "./Code/" + GLOVE_ZIPS[tokens], "-d", "./Code/"])
    subprocess.check_call(["rm", "./Code/" + GLOVE_ZIPS[tokens]])



def set_preferred_glove_model(tokens, vectors):
    if tokens not in GLOVE_FILES:
        raise ValueError(f"Invalid glove tokens: {tokens}")
    
    if vectors not in GLOVE_FILES[tokens]:
        raise ValueError(f"Invalid glove vectors: {vectors}")
    
    if not glove_installed(tokens, vectors):
        raise FileNotFoundError(f"Missing GloVe file: {GLOVE_FILES[tokens][vectors]}")
    
    save = load_data()
    save["preferredModel"]["tokens"] = tokens
    save["preferredModel"]["vectors"] = vectors
    save_data(save)

def get_preferred_glove_model():
    save = load_data()
    model = save["preferredModel"]
    return model