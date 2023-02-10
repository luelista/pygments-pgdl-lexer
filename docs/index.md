## Usage

To use in your documentation, add a `pip install git+https://github.com/luelista/pygments-pgdl-lexer.git` command to your build process.

Then add code snippets with a `pgdl` language marker to your markdown:

````
``` pgdl
My_Type struct {}
```
````


## Examples

```pgdl
datum struct {
			_bitfeld bits(endianness=">", hide=1) {
				year_lo :  3
				day     :  5
				year_hi :  4
				month   :  4
			}
			year NONE(value=(2000 + (_bitfeld.year_hi << 3) + _bitfeld.year_lo), hide=1)
			datum NONE(value=(str(_bitfeld.day) + "." + str(_bitfeld.month) + "." + str(year)))
		}
```

```pgdl
a foo(x=(${aaa}), y=($bbb))
```

### PCAP definition

```pgdl
pcap_file variant {
	struct (endianness="<", section="pcap file, little endian"){
		header pcap_header
		packets repeat pcap_packet
	}
	struct (endianness=">", section="pcap file, big endian"){
		header pcap_header
		packets repeat pcap_packet
	}
	struct (endianness="<", section="pcapNG file, little endian"){
		first_block pcapng_first_block
		rest_blocks repeat pcapng_block
	}
	struct (endianness=">", section="pcapNG file, big endian"){
		first_block pcapng_first_block
		rest_blocks repeat pcapng_block
	}
}

pcap_header struct (section="pcap file header"){
	magic_number UINT32(description="'A1B2C3D4' means the endianness is correct", magic=2712847316)
	version_major UINT16(description="major number of the file format")
	version_minor UINT16(description="minor number of the file format")
	thiszone INT32(description="correction time in seconds from UTC to local time (0)")
	sigfigs UINT32(description="accuracy of time stamps in the capture (0)")
	snaplen UINT32(description="max length of captured packed (65535)")
	encap_proto UINT32(description="type of data link (1 = ethernet)")
}

pcap_packet struct {
	pheader struct (section="pcap packet header"){
		ts_sec UINT32(description="timestamp seconds")
		ts_usec UINT32(description="timestamp microseconds")
		incl_len UINT32(description="number of octets of packet saved in file")
		orig_len UINT32(description="actual length of packet")
	}
	payload BYTES[pheader.incl_len]
}

pcapng_first_block struct (section="pcapNG first block"){
	block_type UINT32(magic=0x0A0D0D0A, color="#999900", show="0x%08X")
	block_length UINT32(color="#666600")
	block_payload struct {
		byte_order_magic UINT32(magic=439041101, color="green", show="0x%08X")
		version_major UINT16
		version_minor UINT16
		section_length INT64
		options BYTES[block_length-28](parse_with=pcapng_options)
	}
	block_length2 UINT32(color="#666600")
}

pcapng_block struct (section="pcapNG block"){
	block_type UINT32(color="#999900", show="0x%08X")
	block_length UINT32(color="#666600")
	block_payload BYTES[block_length - 12](parse_with=pcapng_block_payload)
	block_length2 UINT32(color="#666600")
}

pcapng_block_payload switch block_type {
	case 0x0A0D0D0A: pcapng_SHB
	case 1: pcapng_IDB
	case 3: pcapng_SPB
	case 5: BYTES
	case 6: pcapng_EPB
}

pcapng_SHB struct {
	byte_order_magic UINT32(magic=439041101, color="green", show="0x%08X")
	version_major UINT16
	version_minor UINT16
	section_length INT64
	options pcapng_options
}

pcapng_IDB struct {
	linktype UINT16
	reserved UINT16
	snaplen UINT32
	options pcapng_options
}

pcapng_EPB struct {
	interface_id UINT32
	timestamp_hi UINT32
	timestamp_lo UINT32
	cap_length UINT32
	orig_length UINT32
	payload BYTES[cap_length]
	payload_padding BYTES[pad(4)](textcolor="#888888")
}

pcapng_SPB struct {
	orig_length UINT32
	payload BYTES[block_length - 16]
	payload_padding BYTES[pad(4)](textcolor="#888888")
}

pcapng_options repeat struct {
		code UINT16(color="#660666")
		length UINT16
		value BYTES[length](textcolor="#d3ebff")
		padding BYTES[pad(4)](textcolor="#666")
	}
```

