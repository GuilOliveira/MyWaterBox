vert_shader = '''
#version 420 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 420 core

// Bind the UBO to the same binding point as in the Python code
layout(std140, binding = 0) uniform ParticleData {
    vec4 pos[1000]; // Use the appropriate size for the array
} particles;

in vec2 uvs;
out vec4 f_color;

float sum, xdif, ydif, d, x_to_py, y_to_py, wheight;

uniform sampler2D tex;
uniform int width;
uniform int height;
uniform int list_length;

void main() {
    if(texture(tex, uvs).rgb!=vec3(1,1,1)){
        f_color = vec4(texture(tex, uvs).rgb, 1);
    }else{
    sum = 0.0;
    x_to_py = uvs.x * width;
    y_to_py = uvs.y * height;
    
    for (int i = 0; i < list_length; i++) {
        xdif = x_to_py - particles.pos[i].x;
        ydif = y_to_py - particles.pos[i].y;
        d = sqrt((xdif * xdif) + (ydif * ydif));
        if (d != 0) {
            wheight = 180 * particles.pos[i].z;
            sum += wheight * particles.pos[i].z / (d * d);
        }
    }
    sum = sum / 255;
    if (sum < 0.8) {
        sum = 0.0;
        f_color = vec4(texture(tex, uvs).rgb, 1);
    } else if (sum < 0.85) {
        sum = 0.1;
        f_color = vec4(0,0,0, 1);
    } else {
        sum = 1.0;
        f_color = vec4(0.6,0.6, texture(tex, uvs).b, 1);
    }
    }
    
}

'''