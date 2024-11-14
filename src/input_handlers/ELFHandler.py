import random
import struct
from elftools.elf.elffile import ELFFile
from elftools.elf.sections import SymbolTableSection
import io

class ELFHandler:
    @staticmethod
    def parse_input(content):
        """
        Parses ELF file and returns list of mutated variants
        """
        try:
            # Convert content to bytes if it isn't already
            if isinstance(content, str):
                content = content.encode()
                
            elf_file = ELFFile(io.BytesIO(content))
            return ELFHandler.fuzz(content, elf_file)
        except Exception as e:
            print(f"Error parsing ELF file: {e}")
            return []

    @staticmethod
    def fuzz(original_content, elf_file):
        """
        Applies various mutation strategies to the ELF file
        """
        mutations = []
        
        # Apply different mutation strategies
        mutations.extend(ELFHandler._mutate_elf_header(original_content))
        mutations.extend(ELFHandler._mutate_section_headers(original_content, elf_file))
        mutations.extend(ELFHandler._mutate_program_headers(original_content, elf_file))
        mutations.extend(ELFHandler._mutate_symbol_table(original_content, elf_file))
        mutations.extend(ELFHandler._random_section_mutations(original_content, elf_file))
        
        return mutations

    @staticmethod
    def _mutate_elf_header(content):
        """
        Mutates fields in the ELF header
        """
        mutations = []
        
        # Create copy for mutation
        mutated = bytearray(content)
        
        # Mutate file type with e_type field (bytes 16-17)
        for type_val in range(0, 5):  # Valid ELF types
            mutated[16:18] = struct.pack('H', type_val)
            mutations.append(bytes(mutated))
            
        # Mutate e_machine (bytes 18-19)
        # x86, ARM, x86_64, AArch64, MIPS, RISC-V, Random bytes
        common_machines = [0x03, 0x28, 0x3E, 0xB7, 0x02, 0x3D, 0x69, 0x42, 0x50]
        for machine in common_machines:
            mutated[18:20] = struct.pack('H', machine)
            mutations.append(bytes(mutated))
            
        return mutations

    @staticmethod
    def _mutate_section_headers(content, elf_file):
        """
        Mutates section header table entries
        """
        mutations = []
        mutated = bytearray(content)
        
        # Check if section headers exist
        if not elf_file.has_section_header:
            return mutations
            
        for section in elf_file.iter_sections():
            try:
                # Get section header offset
                sh_offset = section.header.sh_offset
                
                # Ensure we don't go out of bounds
                if sh_offset + 8 > len(content):
                    continue
                    
                # Mutate section type
                mutated[sh_offset:sh_offset + 4] = struct.pack('I', random.randint(0, 11))
                mutations.append(bytes(mutated))
                
                # Mutate section flags
                mutated[sh_offset + 4:sh_offset + 8] = struct.pack('I', random.randint(0, 0xF))
                mutations.append(bytes(mutated))
                
            except Exception as e:
                print(f"Skipping section mutation due to: {e}")
                continue
                
        return mutations

    @staticmethod
    def _mutate_program_headers(content, elf_file):
        """
        Mutates program header table entries to change 
        """
        mutations = []
        mutated = bytearray(content)
        
        for segment in elf_file.iter_segments():
            # Get program header offset
            ph_offset = segment.header.p_offset
            
            # Mutate segment type
            mutated[ph_offset:ph_offset + 4] = struct.pack('I', random.randint(0, 7))
            mutations.append(bytes(mutated))
            
            # Mutate segment flags
            mutated[ph_offset + 4:ph_offset + 8] = struct.pack('I', random.randint(0, 7))
            mutations.append(bytes(mutated))
            
        return mutations

    @staticmethod
    def _mutate_symbol_table(content, elf_file):
        """
        Mutates entries in the symbol table
        """
        mutations = []
        mutated = bytearray(content)
        
        # Check if section headers exist
        if not elf_file.has_section_header:
            return mutations
            
        for section in elf_file.iter_sections():
            try:
                if isinstance(section, SymbolTableSection):
                    for i, symbol in enumerate(section.iter_symbols()):
                        # Get symbol offset
                        sym_offset = section.header.sh_offset + (i * section.header.sh_entsize)
                        
                        # Ensure we don't go out of bounds
                        if sym_offset + 4 >= len(content):
                            continue
                            
                        # Mutate symbol type/binding
                        mutated[sym_offset + 4] = random.randint(0, 15)
                        mutations.append(bytes(mutated))
                        
            except Exception as e:
                print(f"Skipping symbol table mutation due to: {e}")
                continue
                
        return mutations

    @staticmethod
    def _random_section_mutations(content, elf_file):
        """
        Applies random byte flips to specific sections
        """
        mutations = []
        interesting_sections = ['.text', '.data', '.rodata', '.bss']
        
        for section_name in interesting_sections:
            section = elf_file.get_section_by_name(section_name)
            if section:
                mutated = bytearray(content)
                
                # Flip random bytes in section
                for _ in range(10):  # Number of mutations per section
                    offset = random.randint(section.header.sh_offset,
                                         section.header.sh_offset + section.header.sh_size - 1)
                    mutated[offset] ^= random.randint(1, 255)
                    mutations.append(bytes(mutated))
                    
        return mutations 

if __name__ == "__main__":
    with open("./example_inputs/base.bin", "rb") as f:
        print("reading base.bin")
        content = f.read()
        mutations = ELFHandler.parse_input(content)
        print("number of mutations generated:", len(mutations))