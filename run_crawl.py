from crawler import read_playlists_csv, find_all_playlists

def main():
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    except:
        return print("Incorrect arguments passed to script. Script takes 2 arguments - input_filename (String) and output_filename (String).")
    playlists = read_playlists_csv("input/"+input_filename".csv")
    return find_all_playlists(playlists, output_filename)

print("ran_crawl returned with a value: "+main())
