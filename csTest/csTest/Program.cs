using System;
using System.Collections.Generic;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;

namespace csTest
{
	class Program
	{
		public static string Encrypt(string text)
		{
			int x = text.Length % 16;
			if (x != 0)
			{
				for (int i = 0; i < 16 - x; i++)
				{
					text = text + '\0';
				}
			}
			// AesCryptoServiceProvider
			AesCryptoServiceProvider aes = new AesCryptoServiceProvider();
			aes.BlockSize = 128;
			aes.KeySize = 128;
			aes.IV = Encoding.UTF8.GetBytes("68b329da9893e340");
			aes.Key = Encoding.UTF8.GetBytes("68b329da9893e340");
			aes.Mode = CipherMode.ECB;
			aes.Padding = PaddingMode.None;

			// Convert string to byte array
			byte[] src = Encoding.UTF8.GetBytes(text);

			// encryption
			using (ICryptoTransform encrypt = aes.CreateEncryptor())
			{
				byte[] dest = encrypt.TransformFinalBlock(src, 0, src.Length);

				// Convert byte array to Base64 strings
				return Convert.ToBase64String(dest);
			}
		}

		static string Decrypt(string text)
		{
			// AesCryptoServiceProvider
			Rijndael aes = Rijndael.Create();
			aes.BlockSize = 128;
			aes.KeySize = 128;
			aes.IV = Encoding.UTF8.GetBytes("68b329da9893e340");
			aes.Key = Encoding.UTF8.GetBytes("68b329da9893e340");
			aes.Mode = CipherMode.ECB;
			aes.Padding = PaddingMode.None;

			// Convert Base64 strings to byte array
			byte[] src = System.Convert.FromBase64String(text);

			// decryption
			using (ICryptoTransform decrypt = aes.CreateDecryptor())
			{
				byte[] dest = decrypt.TransformFinalBlock(src, 0, src.Length);
				return Encoding.UTF8.GetString(dest);
			}
		}


		static void Main(string[] args)
		{
			string x = Encrypt("hello");
			Console.Write(x);
			string y = Decrypt(x);
			Console.Write(y);
			Console.ReadKey();
		}
	}
}
