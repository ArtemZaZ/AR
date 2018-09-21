uniform mat4 model;
uniform mat4 view;
uniform mat4 perspective;
attribute vec3 position;

void main(void)
{
    gl_Position = perspective * view * model * vec4(position, 1.0);
}
