###### A script for generating a dictionary of class labels for a directory of pngs
# INSTRUCTIONS
# Call the script with an argument to a storage container which can be found in the google sheet:
# Images are loaded in matplotlib and displayed. Display the figure window and the python shell side-by-side to view the images while entering input into the python shell
# User input is requested for every image: 'a'-> label '1'; 's'-> label '0'; 'x'-> exit; '['-> return to the last image (i.e. fix an error); ']'-> advance to the next image (i.e. skip)
# Labels are saved in a json in the image directory: /path/to/images/labels.json and are automatically sent to cloud storage unless the user specifies otherwise.

# For more help with azure cloud storage:
# https://github.com/Azure/azure-storage-python
# https://github.com/Azure-Samples/storage-blobs-python-quickstart

import sys,os, io, time, json, pickle, glob, readchar, argparse

import matplotlib.pyplot as plt 
import matplotlib.image as mpimg
from azure.storage.blob import BlockBlobService

def parse_arguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("dir_name", help="Remote storage container corresponding to the first letter of the country names", type=str)

    # Optional arguments
    parser.add_argument("-d", "--download", help="Download Only.", type=bool, default=False)
    parser.add_argument("-nd","--nodownload", help="Begin labelling without downloading", type=bool, default=False)
    parser.add_argument("-l","--local",help="Local only, i.e. do not upload labels", type=bool, default=False)
    parser.add_argument("-p","--push",help="Push labels only, i.e. do not download or label", type=bool, default=False)
    parser.add_argument("-c","--cleanup",help="Delete all image files after labelling, leaving label files", type=bool, default=False)
    parser.add_argument("-co","--cleanuponly",help="Immediately Delete all image files, leaving label files", type=bool, default=False)


    # Parse arguments
    args = parser.parse_args()

    return args

class Handlabel_Client:

    def __init__(self,dir_name,local_bool):
        self.connection_json = json.load(open('./azure_handlabel.json','r'))
        self.service = BlockBlobService(account_name=self.connection_json['account_name'], account_key=self.connection_json['key'])
        self.dir_name = dir_name # dir_name == remote container_name
        self.cwd = os.getcwd()
        self.local_bool=local_bool
        if not self.local_bool:
            if not self.service.exists(self.dir_name):
                raise Exception('Container does not exist')

    def download(self):
        ### download images for a dir_name

        #mkdir
        if not os.path.exists('./'+self.dir_name):
            os.mkdir(self.dir_name)

        generator = self.service.list_blobs(self.dir_name)
        remote_blobs = [blob.name for blob in generator]
        local_fnames = glob.glob('./'+self.dir_name+'/*.png')

        n_remote_blobs = len(remote_blobs)

        print ('completed %d downloads' % (len(local_fnames)))

        download_blobs = [blob for blob in remote_blobs if blob not in local_fnames]
        n_download_blobs = len(download_blobs)

        for ii_b,blob in enumerate(download_blobs):

            self.service.get_blob_to_path(self.dir_name, blob, os.path.join(self.cwd,self.dir_name,blob))
            sys.stdout.write("\r%d / %d [%s%s]" % ((ii_b+len(local_fnames)),n_remote_blobs,'=' * int((ii_b+len(local_fnames))/n_remote_blobs*20), ' ' * (20-int(ii_b/n_remote_blobs*20))) )    
            sys.stdout.flush()

    def label(self):

        tic = time.time()
        fnames = sorted(glob.glob('./'+self.dir_name+'/*.png'))

        try:
            listodicts = json.load(open('./'+self.dir_name+'/labels.json','r'))
            print ('labels loaded')
        except:
            listodicts = [{'fname':f,'label':None} for f in fnames]
            json.dump(listodicts,open('./'+self.dir_name+'/labels.json','w'))
            print ('writing new labels file')


        fig, axs = plt.subplots(1,1,figsize=(24,12))
        plt.ion()
        plt.show()


        if len([ii for ii in range(len(listodicts)) if listodicts[ii]['label'] is not None])>0:
            ii=max([ii for ii in range(len(listodicts)) if listodicts[ii]['label'] is not None])
        else:
            ii=0

        print ('min ii', ii)
        save_counter = 0

        c = None
        while c!='x' and ii<len(listodicts):

            if os.stat(listodicts[ii]['fname']).st_size==0:
                print ('zero-size file!')
                ii+=1
            else:
                img=mpimg.imread(listodicts[ii]['fname'])
                
                axs.imshow(img)
                #axs.text(0,0,'LABEL: {}'.format(listodicts[ii]['label']))

                print ('Showing sample {:d} / {:d}; LABEL: {}'.format(ii,len(fnames),listodicts[ii]['label']))
                c = input("CHOOSE {'a' -> solar; 's' -> not solar; '[' -> previous image; ']' -> next image; 'x' -> exit}; THEN [enter]")

                if c =='a':
                    listodicts[ii]['label']=1
                    save_counter+=1
                    ii+=1
                elif c =='s':
                    listodicts[ii]['label']=0
                    save_counter+=1
                    ii+=1
                elif c=='[':
                    ii-=1

                elif c==']':
                    ii+=1
                elif c=='x':
                    exit()
                #c = readchar.readchar()
                #print ('save counter',save_counter)
                plt.cla()
                if save_counter%10==0:
                    print ('writing list...')
                    json.dump(listodicts,open('./'+self.dir_name+'/labels.json','w'))
                    if not self.local_bool:
                        self.push_label_json()
                    toc = time.time()-tic
                    print ('time elapsed (s):',toc,'time(s)/ft:',toc/save_counter)

        json.dump(listodicts,open('./'+self.dir_name+'/labels.json','w'))
        if not self.local_bool:
            self.push_label_json()
        toc = time.time()-tic
        #print ('save coun
        print ('time elapsed (s):',toc,'time(s)/ft:',toc/save_counter)

    def push_label_json(self):
        ### push the json labels up
        sys.stdout.write("\ruploading json... " )    
        self.service.create_blob_from_path(self.dir_name, 'labels.json', os.path.join(self.cwd,self.dir_name,'labels.json'))
        sys.stdout.write("done!")
        sys.stdout.flush()
        print('')

    def cleanup(self):
        img_files = glob.glob('./'+self.dir_name+'/*.png')
        for f in img_files:
            os.remove(f)



if __name__ == "__main__":

    args = parse_arguments()

    for a in args.__dict__:
        print(str(a) + ": " + str(args.__dict__[a]))


    client = Handlabel_Client(args.__dict__['dir_name'], args.__dict__['local'])

    
    ##### UI logic
    if args.__dict__['push']:
        ### if push only:
        if not os.path.exists('./'+self.dir_name+'/labels.json'):
            raise Exception('Labels file does not exist!')
        else:
            client.push_label_json()

    elif args.__dict__['cleanuponly']:
        ### cleanup image files only
        client.cleanup()

    elif args.__dict__['download']:
        ### if download only
        client.download()

    elif args.__dict__['nodownload']:
        client.label()
        if args.__dict__['cleanup']:
            client.cleanup()

    else:
        client.download()
        client.label()
        if args.__dict__['cleanup']:
            client.cleanup()