import base64
import gzip

#XOR the stream of bytes with the given key. Returns a stream of bytes 
def Xor(input, key):
    
    output = []
    for byte in input:
        output.append(chr(byte^key))
    return ''.join(output).encode('ascii')

#Decrypt a stream of bytes. Returns the decryted stream of data
def Decryt(encrypted_stream, xor=True):

    #Xor encryption with key 11.
    base64_stream = encrypted_stream
    if xor:
        base64_stream = Xor(encrypted_stream,11)
    
    #Decode with base64. Must replace characters to make it a file safe string
    zipped_stream = base64.b64decode(base64_stream, altchars=b'-_')
    
    #Gzip decompress the stream
    return gzip.decompress(zipped_stream)

#Encrypt a stream of bytes. Returns the encrypted stream of data
def Encrypt(raw_stream, xor=True, compression=6):

    #Gzip compress the raw stream. Must use level 6 compression or it will not be the same
    zipped_stream = gzip.compress(raw_stream, compresslevel=compression)

    #Encode with base64. Must replace characters to make it a file safe string
    base64_stream = base64.b64encode(zipped_stream, altchars=b'-_')
    base64_stream = b'H4sIAAAAAAAAC' + base64_stream[13:]
    
    #Xor encrypt with key 11. Must replace characters to reverse the safe stream
    if xor:
        return Xor(base64_stream, 11)
    else:
        return base64_stream