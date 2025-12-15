import subprocess
import os
import shutil

input_pdf = 'output_60mb.pdf'
compressed_pdf = 'compressed.pdf'
size = 20
output_pdf = f'output_{size}mb.pdf'
target_size = size * 1024 * 1024

def get_size(path):
    return os.path.getsize(path)

def compress_pdf(input_path, output_path):
    subprocess.run([
        'gs', '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        '-dPDFSETTINGS=/screen',
        '-dNOPAUSE', '-dQUIET', '-dBATCH',
        f'-sOutputFile={output_path}',
        input_path
    ], check=True)

def pad_to_target(path, target_bytes):
    with open(path, 'rb') as f:
        data = f.read()
    size = len(data)

    if size < target_bytes:
        # Calculate exact padding needed
        # We'll add: '\n% ' (3 bytes) + padding zeros
        padding_needed = target_bytes - size
        
        if padding_needed >= 3:
            padding_zeros = padding_needed - 3  # Subtract the '\n% ' bytes
            padding = b'\n% ' + b'0' * padding_zeros
        else:
            # If we need less than 3 bytes, just add spaces
            padding = b' ' * padding_needed
            
        with open(output_pdf, 'wb') as f:
            f.write(data)
            f.write(padding)
        print(f'✅ Padded to exactly {get_size(output_pdf) / (1024*1024):.2f} MB')
        
    elif size > target_bytes:
        # Find %%EOF marker
        eof_index = data.rfind(b'%%EOF')
        
        if eof_index != -1 and eof_index + 5 <= target_bytes:
            # Trim right before or after EOF to maintain validity
            # Keep everything up to EOF, then pad to exact size
            trimmed = data[:eof_index + 5]  # Include %%EOF
            remaining = target_bytes - len(trimmed)
            
            with open(output_pdf, 'wb') as f:
                f.write(trimmed)
                if remaining > 0:
                    f.write(b'\n' * remaining)
        else:
            # Can't preserve EOF, just trim (may corrupt PDF)
            trimmed = data[:target_bytes]
            with open(output_pdf, 'wb') as f:
                f.write(trimmed)
                
        print(f'✅ Trimmed to exactly {get_size(output_pdf) / (1024*1024):.2f} MB')
    else:
        shutil.copy(path, output_pdf)
        print('✅ Already exactly 40 MB')

# Step 1: compress
print('🔧 Compressing...')
compress_pdf(input_pdf, compressed_pdf)
print(f'   Compressed size: {get_size(compressed_pdf) / (1024*1024):.2f} MB')

# Step 2: adjust to exact target
pad_to_target(compressed_pdf, target_size)

final_size = get_size(output_pdf)
print(f'🎯 Done → {output_pdf}')
print(f'   Final size: {final_size / (1024*1024):.6f} MB')
print(f'   Exact bytes: {final_size:,} bytes')
print(f'   Target bytes: {target_size:,} bytes')
print(f'   Difference: {final_size - target_size} bytes')