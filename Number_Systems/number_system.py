from manim import *

class NumberSystemExplanation(Scene):
    def construct(self):
        # Title: Introducing the Topic
        title = Text("Understanding Number Systems", font_size=48)
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Definition of a number system.
        definition = Tex(
            r"A \textbf{number system} is a method of representing numbers using a set of symbols (digits).",
            font_size=36,
        )
        definition.next_to(title, DOWN, buff=0.5)
        self.play(Write(definition))
        self.wait(2)

        # Explanation on Base (Radix)
        base_text = Tex(
            r"The \textbf{base} (or \textbf{radix}) determines the number of unique digits used.",
            font_size=36,
        )
        base_text.next_to(definition, DOWN, buff=0.8)
        self.play(Write(base_text))
        self.wait(2)

        # Examples of digits in various bases.
        decimal_digits = Tex(
            r"Decimal (Base 10):\quad 0, 1, 2, 3, 4, 5, 6, 7, 8, 9", font_size=36
        )
        decimal_digits.next_to(base_text, DOWN, buff=0.8)
        self.play(Write(decimal_digits))
        self.wait(2)

        binary_digits = Tex(
            r"Binary (Base 2):\quad 0, 1", font_size=36
        )
        binary_digits.next_to(decimal_digits, DOWN, buff=0.8)
        self.play(Write(binary_digits))
        self.wait(2)

        hex_digits = Tex(
            r"Hexadecimal (Base 16):\quad 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, A, B, C, D, E, F",
            font_size=36,
        )
        hex_digits.next_to(binary_digits, DOWN, buff=0.8)
        self.play(Write(hex_digits))
        self.wait(2)

        # Fade out the definition and base text.
        self.play(FadeOut(definition), FadeOut(base_text))
        self.wait(1)
        
        # Fade out the digit examples.
        self.play(FadeOut(decimal_digits), FadeOut(binary_digits), FadeOut(hex_digits))
        self.wait(1)
        
    
        
        # Introduce counting in different bases.
        counting_title = Text("Counting in Different Bases", font_size=42)
        counting_title.to_edge(LEFT)
        self.play(FadeIn(counting_title))
        self.wait(1)

        # Decimal counting animation.
        decimal_count = VGroup(
            Tex("7", font_size=36),
            Tex("8", font_size=36),
            Tex("9", font_size=36),
            Tex("10", font_size=36),
        ).arrange(RIGHT, buff=1)
        decimal_count.next_to(counting_title, RIGHT, buff=1)
        self.play(Write(decimal_count))
        self.wait(2)
        
        # Show the explanation for decimal counting.
        self.play(FadeOut(counting_title))
        self.wait(1)

        explanation_decimal = Tex(r"$10 = 1 \times 10 + 0$", font_size=36)
        explanation_decimal.next_to(decimal_count, DOWN, buff=0.5)
        self.play(Write(explanation_decimal))
        self.wait(2)

        # Binary counting animation.
        binary_count = VGroup(
            Tex("0", font_size=36),
            Tex("1", font_size=36),
            Tex("10", font_size=36),
        ).arrange(RIGHT, buff=1)
        binary_count.next_to(explanation_decimal, DOWN, buff=1.5)
        self.play(Write(binary_count))
        self.wait(2)

        explanation_binary = Tex(r"$10_{2} = 1 \times 2 + 0$", font_size=36)
        explanation_binary.next_to(binary_count, DOWN, buff=0.5)
        self.play(Write(explanation_binary))
        self.wait(2)
        
        # Fade out the counting examples.
        self.play(FadeOut(decimal_count), FadeOut(explanation_decimal), FadeOut(binary_count), FadeOut(explanation_binary))
        self.wait(1)

        # Conversion Example: Decimal to Binary
        conversion_title = Text("Decimal to Binary Conversion", font_size=42)
        conversion_title.to_edge(UP)
        self.play(Transform(title, conversion_title))
        self.wait(1)

        # Show step-by-step division by 2.
        conversion_steps = VGroup(
            Tex(r"$13 \div 2 = 6 \quad \text{remainder } 1$", font_size=36),
            Tex(r"$6 \div 2 = 3 \quad \text{remainder } 0$", font_size=36),
            Tex(r"$3 \div 2 = 1 \quad \text{remainder } 1$", font_size=36),
            Tex(r"$1 \div 2 = 0 \quad \text{remainder } 1$", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        conversion_steps.next_to(conversion_title, DOWN, buff=1)
        self.play(Write(conversion_steps))
        self.wait(3)

        conversion_result = Tex(r"$13_{10} = 1101_{2}$", font_size=36)
        conversion_result.next_to(conversion_steps, DOWN, buff=1)
        self.play(Write(conversion_result))
        self.wait(3)

        # Fade out the conversion example.
        self.play(FadeOut(conversion_title), FadeOut(conversion_steps), FadeOut(conversion_result))
        self.wait(1)
        
        # Conversion Example: Decimal to Hexadecimal
        conversion_title_hex = Text("Decimal to Hexadecimal Conversion", font_size=42)
        conversion_title_hex.to_edge(UP)
        self.play(Transform(title, conversion_title_hex))
        self.wait(1)

        hex_conversion_steps = VGroup(
            Tex(r"$13 \div 16 = 0 \quad \text{remainder } 13$", font_size=36),
            Tex(r"$13 \text{ in hex is } D$", font_size=36),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        hex_conversion_steps.next_to(conversion_title_hex, DOWN, buff=1)
        self.play(Write(hex_conversion_steps))
        self.wait(3)

        hex_conversion_result = Tex(r"$13_{10} = D_{16}$", font_size=36)
        hex_conversion_result.next_to(hex_conversion_steps, DOWN, buff=1)
        self.play(Write(hex_conversion_result))
        self.wait(3)
        
        # Fade out the conversion example.
        self.play(FadeOut(conversion_title_hex), FadeOut(hex_conversion_steps), FadeOut(hex_conversion_result))
        self.wait(1)

        # Concluding message.
        conclusion = Text(r"Number systems are fundamental to mathematics and computing.", font_size=26)
        conclusion.to_edge(DOWN)
        self.play(FadeIn(conclusion))
        self.wait(3)

        # Fade out all objects.
        all_objects = VGroup(
            title, definition, base_text, decimal_digits, binary_digits,
            hex_digits, counting_title, decimal_count, explanation_decimal,
            binary_count, explanation_binary, conversion_steps, conversion_result,
            hex_conversion_steps, hex_conversion_result, conclusion
        )
