uniform mat4 model;
uniform mat4 view;
uniform mat4 perspective;
attribute vec3 position;
attribute vec4 color;
varying vec4 vColor;

void main(void)
{
    vColor = color;
    gl_Position = perspective * view * model * vec4(position, 1.0);
}
