.model small
.stack
.data

n1 db ?

.code
main proc
mov ax, @data
mov ds, ax
print macro s
mov ah, 9
lea dx, s
int 21h
endm

call read_num
mov n1, al
mov al 2
add n1 al
mov ax n1
call print_num

int 27h
main endp

print_num proc
mov cx, 0
mov bl, 10
mov ah, 0
next_digit:
div bl
add ah, '0'
push ax
inc cx
mov ah, 0
test al, al
jnz next_digit
print_digits:
pop dx
mov dl, dh
mov ah, 2h
int 21h
loop print_digits
mov ah, 2
mov dx, 10
int 21h
ret
print_num endp

read_num proc
mov bx, 10
push bx
xor bx, bx
mov cx, 1
mov si, 0
_read1:
cmp si, 3
jge _auto_nl

mov ah, 1
int 21h
cmp al, 13
je _read2
cmp al, '0'
jb _read1
cmp al, '9'
ja _read1

inc si
mov ah, 0
push ax
jmp _read1

_auto_nl:
mov ah, 2
mov dl, 10
int 21h
_read2:
pop dx
cmp dx, 10
je _end_read
sub dl, '0'
mov ax, dx
mul cx
add bx, ax
mov ax, cx
mov dx, 10
mul dx
mov cx, ax
jmp _read2

_end_read:
mov ax, bx
ret
read_num endp
end