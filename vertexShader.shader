uniform mat4 model;
uniform mat4 view;
uniform mat4 perspective;
attribute vec3 position;
attribute vec4 color;
attribute vec2 textCoord;

varying vec4 vColor;
varying vec2 vTextCoord;

void main(void)
{
    vColor = color;
    vTextCoord = textCoord;
    gl_Position = perspective * view * model * vec4(position, 1.0);
}
