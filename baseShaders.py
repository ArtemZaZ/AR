baseSpriteVertexShader = """
attribute vec2 vertex;
attribute vec2 textureCoordinates;
varying vec2 vTextCoordinates;

void main(void)
{
    vTextCoordinates = textureCoordinates;
    gl_Position = vec4(vertex, 0.0, 1.0);
}
"""

baseSpriteFragmentShader = """
varying vec2 vTextCoordinates;
uniform sampler2D sampleTexture;

void main()
{
    gl_FragColor = texture(sampleTexture, vTextCoordinates);
}
"""