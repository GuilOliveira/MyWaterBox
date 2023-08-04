vert_shader = '''
#version 400 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 400 core

const int MAX = 1000 ;

uniform sampler2D tex;
uniform int width;
uniform int height;
uniform int list_length;
uniform vec3 particle_list[MAX];

in vec2 uvs;
out vec4 f_color;

float sum, xdif, ydif, d, x_to_py, y_to_py;

void main() {
    sum = 0.0;
    x_to_py = uvs.x*width;
    y_to_py = uvs.y*height;

    for(int i=0;i<list_length;i++){
        xdif = x_to_py - particle_list[i].x;
        ydif = y_to_py - particle_list[i].y;
        d = sqrt((xdif * xdif) + (ydif * ydif));
        if (d!=0){
            sum += 30*particle_list[i].z/d;
            
        }
    }
    sum=sum/255;
    if(sum<0.795){
        sum=0.0;
        }else if(sum<0.8){
        sum=0.1;
        }else{
        sum=1.0;
        }

    f_color = vec4(texture(tex, uvs).rg*(1-sum),texture(tex, uvs).b, 1);
}
'''