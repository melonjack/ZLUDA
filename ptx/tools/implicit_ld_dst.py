import os
import subprocess
import tempfile

types = ["b8", "b16", "b32", "b64", "u8", "u16", "u32", "u64", "s8", "s16", "s32", "s64", "f32", "f64"]

for op_type in types:
    for output_type in types:
        with tempfile.TemporaryDirectory() as dir:
            f_name = os.path.join(dir, 'ptx')
            out_name = os.path.join(dir, 'out')
            with open(f_name, 'w') as f:
                f.write(
                f"""
                .version 6.5
                .target sm_30
                .address_size 64
                .visible .entry VecAdd_kernel(
                    .param .{op_type} input
                )
                {{
                    .reg.{output_type}        r1;
                    ld.param.{op_type} 	r1, [input];
                    ret;
                }}
                """)
            err = subprocess.run(f"ptxas {f_name} -o {out_name}", capture_output = True)
            if err.returncode == 0:
                print(f"{op_type} {output_type}")
            else:
                print(f"[INVALID] {op_type} {output_type}")