import java.security.KeyPairGenerator;
import java.security.Signature;
class LegacyCrypto {
    void setup() throws Exception {
        KeyPairGenerator rsa = KeyPairGenerator.getInstance("RSA");
        Signature signature = Signature.getInstance("SHA256withECDSA");
    }
}
