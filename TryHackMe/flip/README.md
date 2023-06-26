# Flip

#### Step-by-step walkthrough and explanation for the 'Flip' room! c:

<br /><br />

<p align="center">
    <img src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/a774e125-f1b9-4222-b9f1-9cb93d7a1a8d" alt="Flip">
</p>

<br />

## Sections

- Initial Info
- Preliminary Testing
- Research
- Implementation

<br /><br /><br />

<img width=1000 src="https://user-images.githubusercontent.com/110672478/213883818-2d61fe01-de6b-449a-95c3-c20947fb4d33.gif"  alt="cool line art c:">

## Initial Info

The info provided isn't very helpful at all, which does make it a bit more fun c:

<br /><br />

- Initially make sure to download the task files consisting of a singular python script!
- Then make sure to press the `Completed` button so that you get full credit for completing the room c:

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/0f385d3a-1d39-4267-a459-dd68552c1f08" alt="First steps">
</p>

<br />

It looks like we'll have to connect to the server using `netcat`, at least that's the shell I'll be using in this writeup c:

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/410c29b0-80ca-45da-8c24-7aa7e343a97e" alt="First steps">
</p>

<br />

**So let's connect!**

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/80866bba-457a-472e-bc89-00d79dbbe5fa" alt="First steps">
</p>

<br />

Let's refrain from inputting anything yet until the next section c:

<br /><br /><br />

## Preliminary Testing

<br />

**Let's look at the task file we got!**

I'll be using neovim but you can use an editor of your choice (or even just `cat` since it's just the source code!)

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/f2dd0e4e-9a23-4196-badb-4305239631ee" alt="Server source code" >
</p>

This may seem like a lot but there's really only a few sections we need to pay attention to here.

First, lets take a look at the imports:

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/fe543031-9700-4ce0-98a0-a8cabab8453e" alt="Imports" >
</p>

Here we can see we're going to be dealing with `AES encryption`, `padding`, and `hexadecimal`. But this is a very high level overview of things.

<br />

Next, I'm sure this is eye catching, seemingly login credentials for the server!

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/c3f874c9-cde4-41cf-937b-46cdaedc1f5c" alt="Fake creds" >
</p>

However, if we look closer this seems to be a red herring :c

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/7a7b28ae-97c0-4905-bc13-417d4fad94df" alt="nyoooo!!!" >
</p>

Let's keep those creds in mind though, as we may use them later!

<br /><br />

For now, lets move on:

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/88ae01c8-a07a-4cec-9479-5b40bb6675a1" alt="Algorithm" >
</p>

It appears we've stumbled across the cryptgraphic algorithm it's using! CBC, cipher block chaining, is the most popular block cipher model algorithm! Furthermore, it appears it's using a padding of 16 bytes c:

<br />

It also appears it's using 16 bytes randomly assigned for the IV, inialization vector, and it's cryptographic key.

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/43098082-f15d-4617-9418-227bc1fa418f" alt="Key and IV size" >
</p>

<br />

It appears we've also identified how it's formatting it's plaintext message! That'll be great for future use!

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/9a4b9708-d451-4198-a42f-fd26d65fd192" alt="Plaintext Format" >
</p>

<br />

Great, we've identified the algorithms and methods used, discovered a pitfall, and got some creds we can potentially play with as well as learned how to pass them!

<br /><br /><br />

## Research

<br />

<p>
    Given what we learned in the 'Preliminary Testing' section we can safely gather that the server is implementing a <a href="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)" target="_blank">CBC (Cipher Block Chaining)</a> algorithm.
</p>

<br />
<p align="center">
    <img src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/e961332c-5f52-4bf2-8bff-d4cde76c7328" alt="CBC Encryption" href="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)" target="_blank">
    <br /><br />
    <img src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/6da336be-3a1e-4ab1-9fda-fe5edbbb45de" href="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation" alt="CBC Decryption" href="https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_block_chaining_(CBC)" target="_blank">
</p>
<br />

<p>
    For better understanding, this visual diagram represents the CBC cryptographic algorithm in a relatively understandable way.
</p>

<p>
    For a verbal description—each pass will XOR the next 16 byte segment with the current 16 byte segment and then it will be encrypted with the random data.
</p>

<br />

<p>
    Since we know that the server will detect our creds with a hardcoded check lets ever so slightly obfuscate them:
</p>

```
access_username=bdmin&password=sUp3rPaSs1
```

<p>
    We will input our modified login we derived from our code analysis previously like so:
</p>

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/74562fd0-f3c4-4c5b-b08a-2e39d908d43c" alt="Leaked Cipher Text">
</p>

<p>
    As we know our input will be cut and padded, into 16 byte segments as such: 
</p>

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/cd810139-1040-4089-b73d-b14568a7ae42" alt="Padding">
</p>

<p>
    Next we need to break our hex ciphertext string we got from our input into 3x32 byte segments for visual clarity:
</p>

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/02c6a150-4b80-4fbb-affb-cb7a5f067e48" alt="Padding">
</p>

<br /><br />

<hr />

From now on we'll be using a mathematical notation for XOR represented as: `⊕`

<br />

<p> As a sidenote, here's a handy lil way of doing hexadecimal XOR operations locally from the terminal c:

<p align="center">
    <img style="-webkit-filter: drop-shadow(12px 12px 7px rgba(0,0,0,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/cb9e699e-7362-4091-b7f3-04c71e92a9cc" alt="Python hex!">
</p>
<hr />
<br /><br />

<p>
    Because we control the input, regardless of the encryption we know what the initial values of the first 2 segments are and subsequently what they are after being encrypted:
</p>

```
'a' ⇒ 0x0b
'b' ⇒ 0x5e
```

<p align="center" style="font-size: 10px">
    <em>(if confused, reference the initial image showing the padding and segmenting applied to our input)</em>
</p>

<p>
    Because we know that each pass will be used to XOR the next we can use some basic algebraic principles by isolating variables:
</p>

<p align="center" style="font-size: 8px">
    <em>(0x5e, our 'b', will be enclosed in curly braces as it's encrypted and will be the variable we're isolating)</em>
</p>
<br />

```
0x0b ⊕ {0x5e} ⇒ 'b' ⇒ 0x62
```

<p align="center" style="font-size: 9px">
    <em>(The way we get 0x62 here is by referencing the hex value for 'b' in the ascii table)</em>
</p>

<br />

```
0x0b ⊕ 0x62 ⇒ {0x5e} ⇒ 0x69
```

<br />

<p>
    Now we <strong>finally</strong> have something to work with! Just a bit more XOR calculations and we'll be on our way to finishing the room!
</p>

We'll be decrementing our `0x62` hex value for 'b' to get our hex value for 'a' `0x61`!

<p>
    <strong>NOW</strong> for our final XOR! ~
</p>

```
0x69 ⊕ 0x61 ≡ 0x08
```

<br /><br />

<h1 align="center">
    YAYYY!
</h1>

<br /><br />

<p align="center">
    Now, finally, we replace our first hex value 0x0b with our output of 0x08 and........
</p>

<br />

<p align="center">
    <img style="-webkit-filter: drop-shadow(10px 10px 7px rgba(128,0,128,0.5));" src="https://github.com/NaomiTesla/ctf-writeups/assets/110672478/47509c68-016a-4645-a304-ee87ebe7725e" alt="flag!!!">
</p>

<br /><br />

<h1 align="center">
    CONGRATULATIONS!
</h1>

<img width=1000 src="https://user-images.githubusercontent.com/110672478/213883818-2d61fe01-de6b-449a-95c3-c20947fb4d33.gif"  alt="cool line art c:">

<br /><br />
