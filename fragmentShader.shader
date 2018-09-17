varying vec4 vColor;
varying vec2 vTextCoord;

uniform sampler2D sampleText;
void main()
{
    vColor;
    gl_FragColor = texture(sampleText, vTextCoord);
    //gl_FragColor = vColor;
}