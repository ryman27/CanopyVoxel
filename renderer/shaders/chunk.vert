#version 330 core

layout (location = 0) in ivec3 in_position;
layout (location = 1) in ivec3 voxel_color_in;
layout (location = 2) in int face_id;

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

out vec3 voxel_color;
out vec2 uv;

const vec2 uv_coords[4] = vec2[4](
    vec2(0, 0), vec2(0, 1),
    vec2(1, 0), vec2(1, 1)
);

const int uv_indices[12] = int[12](
    1, 0, 2, 1, 2, 3,  // tex coords indices for vertices of an even face
    3, 0, 2, 3, 1, 0   // odd face
);

vec3 normalize_color(vec3 vec){
    vec3 p3 = vec.xyz / 255.0; // Normalize color values to the range [0.0, 1.0]
    return p3;
}

vec3 gray_scale(ivec3 vec){
    float gray = dot(vec.xyz, vec3(0.2126, 0.7152, 0.0722));
    return vec3(gray);
}


void main() {
    int uv_index = gl_VertexID % 6  + (face_id & 1) * 6;
    uv = uv_coords[uv_indices[uv_index]];
    voxel_color = normalize_color(voxel_color_in);
    gl_Position = projection * view * model * vec4(in_position, 1.0);
}







































