#version 330 compatibility

uniform vec3 Light_location;


out vec3 vN;
out vec3 vL;
out vec3 vE;
out vec2 vST;


void main() {
	vST = gl_MultiTexCoord0.st;

	vec4 ECPosition = gl_ModelViewMatrix * gl_Vertex;
	
	vN = normalize(gl_NormalMatrix * gl_Normal);
	vL = Light_location - ECPosition.xyz;
	
	vE = vec3(0.,0.,0.) - ECPosition.xyz;
	gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}